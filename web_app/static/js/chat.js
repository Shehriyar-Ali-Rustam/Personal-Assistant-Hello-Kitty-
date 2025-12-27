/**
 * Hello Kitty Web Chat - JavaScript
 * Handles chat functionality with streaming responses and voice support
 */

// State
let isTyping = false;
let chatHistory = [];
let isRecording = false;
let voiceOutputEnabled = true;
let recognition = null;
let synthesis = window.speechSynthesis;

// Voice Mode State
let voiceModeActive = false;
let voiceModeListening = false;
let voiceModeRecognition = null;

// Wake Word Detection State
let wakeWordEnabled = false;
let wakeWordRecognition = null;
let isProcessingCommand = false;
const WAKE_WORD = "hello kitty";

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const welcomeScreen = document.getElementById('welcomeScreen');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Load voice preference
    voiceOutputEnabled = localStorage.getItem('voiceOutput') !== 'false';
    updateVoiceToggleIcon();

    // Initialize speech recognition
    initSpeechRecognition();

    // Load chat history from localStorage
    loadChatHistory();

    // Focus input
    messageInput.focus();
});

// Initialize Speech Recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
    } else if ('SpeechRecognition' in window) {
        recognition = new SpeechRecognition();
    } else {
        console.warn('Speech recognition not supported');
        const micBtn = document.getElementById('micBtn');
        if (micBtn) micBtn.style.display = 'none';
        return;
    }

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isRecording = true;
        updateMicButton(true);
        setVoiceStatus('Listening...', 'listening');
    };

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        // Show interim results in input
        if (interimTranscript) {
            messageInput.value = interimTranscript;
            setVoiceStatus('Listening: ' + interimTranscript.substring(0, 30) + '...', 'listening');
        }

        // Send final result
        if (finalTranscript) {
            messageInput.value = finalTranscript;
            setVoiceStatus('');
            stopRecording();
            // Auto-send the message
            setTimeout(() => sendMessage(), 300);
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        stopRecording();

        if (event.error === 'not-allowed') {
            setVoiceStatus('Microphone access denied. Please allow microphone.', 'error');
        } else if (event.error === 'no-speech') {
            setVoiceStatus('No speech detected. Try again.', 'error');
        } else {
            setVoiceStatus('Error: ' + event.error, 'error');
        }

        setTimeout(() => setVoiceStatus(''), 3000);
    };

    recognition.onend = () => {
        stopRecording();
    };
}

// Toggle Voice Input (Microphone)
function toggleVoiceInput() {
    if (!recognition) {
        setVoiceStatus('Speech recognition not supported in this browser', 'error');
        setTimeout(() => setVoiceStatus(''), 3000);
        return;
    }

    if (isRecording) {
        recognition.stop();
        stopRecording();
    } else {
        try {
            recognition.start();
        } catch (e) {
            console.error('Error starting recognition:', e);
            setVoiceStatus('Error starting microphone', 'error');
            setTimeout(() => setVoiceStatus(''), 3000);
        }
    }
}

// Stop Recording
function stopRecording() {
    isRecording = false;
    updateMicButton(false);
}

// Update Mic Button State
function updateMicButton(recording) {
    const micBtn = document.getElementById('micBtn');
    if (micBtn) {
        if (recording) {
            micBtn.classList.add('recording');
        } else {
            micBtn.classList.remove('recording');
        }
    }
}

// Set Voice Status Message
function setVoiceStatus(message, type = '') {
    const voiceStatus = document.getElementById('voiceStatus');
    if (voiceStatus) {
        voiceStatus.textContent = message;
        voiceStatus.className = 'voice-status' + (type ? ' ' + type : '');
    }
}

// Toggle Voice Output (Text-to-Speech)
function toggleVoiceOutput() {
    voiceOutputEnabled = !voiceOutputEnabled;
    localStorage.setItem('voiceOutput', voiceOutputEnabled);
    updateVoiceToggleIcon();

    if (voiceOutputEnabled) {
        setVoiceStatus('Voice responses enabled');
    } else {
        setVoiceStatus('Voice responses disabled');
        // Stop any current speech
        synthesis.cancel();
    }
    setTimeout(() => setVoiceStatus(''), 2000);
}

// Update Voice Toggle Icon
function updateVoiceToggleIcon() {
    const voiceToggleBtn = document.getElementById('voiceToggleBtn');
    const speakerIcon = document.getElementById('speakerIcon');

    if (voiceToggleBtn && speakerIcon) {
        if (voiceOutputEnabled) {
            voiceToggleBtn.classList.add('active');
            voiceToggleBtn.classList.remove('muted');
            speakerIcon.innerHTML = `
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            `;
        } else {
            voiceToggleBtn.classList.remove('active');
            voiceToggleBtn.classList.add('muted');
            speakerIcon.innerHTML = `
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <line x1="23" y1="9" x2="17" y2="15"></line>
                <line x1="17" y1="9" x2="23" y2="15"></line>
            `;
        }
    }
}

// Speak Text (Text-to-Speech)
function speakText(text) {
    if (!voiceOutputEnabled || !synthesis) return;

    // Cancel any ongoing speech
    synthesis.cancel();

    // Clean text for speech
    const cleanText = text
        .replace(/```[\s\S]*?```/g, 'code block')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .replace(/\*([^*]+)\*/g, '$1')
        .replace(/<[^>]*>/g, '')
        .replace(/&[^;]+;/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.1; // Slightly higher pitch for Hello Kitty
    utterance.volume = 1.0;

    // Try to find a female voice
    const voices = synthesis.getVoices();
    const femaleVoice = voices.find(v =>
        v.name.includes('Female') ||
        v.name.includes('Samantha') ||
        v.name.includes('Victoria') ||
        v.name.includes('Karen') ||
        v.name.includes('Moira')
    ) || voices.find(v => v.lang.startsWith('en')) || voices[0];

    if (femaleVoice) {
        utterance.voice = femaleVoice;
    }

    synthesis.speak(utterance);
}

// Send Message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;

    // Hide welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }

    // Add user message
    addMessage('user', message);

    // Clear input
    messageInput.value = '';
    autoResize(messageInput);

    // Show typing indicator
    isTyping = true;
    sendBtn.disabled = true;
    const typingId = showTypingIndicator();

    try {
        // Use streaming endpoint
        const response = await fetch('/api/chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        // Create assistant message element
        const messageElement = createMessageElement('assistant', '');
        chatMessages.appendChild(messageElement);
        const textElement = messageElement.querySelector('.message-text');

        // Read streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        if (data.content) {
                            fullResponse += data.content;
                            textElement.innerHTML = formatMessage(fullResponse);
                            scrollToBottom();
                        }
                        if (data.error) {
                            textElement.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
                        }
                    } catch (e) {
                        // Ignore parse errors for incomplete chunks
                    }
                }
            }
        }

        // Speak the response
        speakText(fullResponse);

        // Save to history
        chatHistory.push({ role: 'user', content: message });
        chatHistory.push({ role: 'assistant', content: fullResponse });
        saveChatHistory();

    } catch (error) {
        removeTypingIndicator(typingId);
        const errorMsg = 'Sorry, I had trouble responding. Please try again!';
        addMessage('assistant', errorMsg);
        speakText(errorMsg);
        console.error('Error:', error);
    } finally {
        isTyping = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

// Add Message to Chat
function addMessage(role, content) {
    const messageElement = createMessageElement(role, content);
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Create Message Element
function createMessageElement(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const avatarContent = role === 'user' ? '👤' : '🎀';
    const name = role === 'user' ? 'You' : 'Hello Kitty';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatarContent}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-name">${name}</span>
                <span class="message-time">${timeStr}</span>
            </div>
            <div class="message-text">${formatMessage(content)}</div>
        </div>
    `;

    return messageDiv;
}

// Format Message (handle markdown-like syntax)
function formatMessage(text) {
    if (!text) return '';

    // Escape HTML
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Code blocks
    formatted = formatted.replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

    // Inline code
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold
    formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Italic
    formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');

    return formatted;
}

// Show Typing Indicator
function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = id;
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = `
        <div class="message-avatar">🎀</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return id;
}

// Remove Typing Indicator
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

// Scroll to Bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle Key Down
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Auto Resize Textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

// Send Quick Prompt
function sendQuickPrompt(prompt) {
    messageInput.value = prompt;
    sendMessage();
}

// Reset Conversation
async function resetConversation() {
    try {
        // Stop any ongoing speech
        synthesis.cancel();

        await fetch('/api/reset', { method: 'POST' });

        // Clear UI
        chatMessages.innerHTML = '';
        chatHistory = [];
        saveChatHistory();

        // Show welcome screen
        chatMessages.innerHTML = `
            <div class="welcome-screen" id="welcomeScreen">
                <div class="welcome-icon">🎀</div>
                <h2>Hello! I'm Hello Kitty</h2>
                <p>Your friendly AI assistant. How can I help you today?</p>
                <div class="quick-prompts">
                    <button class="quick-prompt" onclick="sendQuickPrompt('What is the weather today?')">
                        <span class="prompt-icon">🌤️</span>
                        <span>Check Weather</span>
                    </button>
                    <button class="quick-prompt" onclick="sendQuickPrompt('What time is it?')">
                        <span class="prompt-icon">🕐</span>
                        <span>Current Time</span>
                    </button>
                    <button class="quick-prompt" onclick="sendQuickPrompt('Tell me a joke')">
                        <span class="prompt-icon">😄</span>
                        <span>Tell a Joke</span>
                    </button>
                    <button class="quick-prompt" onclick="sendQuickPrompt('What can you do?')">
                        <span class="prompt-icon">✨</span>
                        <span>What can you do?</span>
                    </button>
                </div>
            </div>
        `;

        messageInput.focus();
    } catch (error) {
        console.error('Error resetting conversation:', error);
    }
}

// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('visible');
}

// Toggle Theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

// Update Theme Icon
function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('themeIcon');
    if (theme === 'dark') {
        themeIcon.innerHTML = `
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
    } else {
        themeIcon.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        `;
    }
}

// Save Chat History to localStorage
function saveChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    } catch (e) {
        console.error('Error saving chat history:', e);
    }
}

// Load Chat History from localStorage
function loadChatHistory() {
    try {
        const saved = localStorage.getItem('chatHistory');
        if (saved) {
            chatHistory = JSON.parse(saved);
            if (chatHistory.length > 0) {
                // Hide welcome screen
                if (welcomeScreen) {
                    welcomeScreen.style.display = 'none';
                }

                // Render messages
                chatHistory.forEach(msg => {
                    addMessage(msg.role, msg.content);
                });
            }
        }
    } catch (e) {
        console.error('Error loading chat history:', e);
        chatHistory = [];
    }
}

// Load voices when available
if (synthesis) {
    synthesis.onvoiceschanged = () => {
        // Voices are now loaded
    };
}

// ==========================================
// VOICE MODE - Continuous Voice Conversation
// ==========================================

// Enter Voice Mode
function enterVoiceMode() {
    voiceModeActive = true;
    const overlay = document.getElementById('voiceModeOverlay');
    overlay.classList.add('active');

    // Initialize voice mode recognition
    initVoiceModeRecognition();

    // Greet the user
    setVoiceModeStatus('Click the microphone to start talking', '');

    // Auto-start listening after a brief delay
    setTimeout(() => {
        startVoiceModListening();
    }, 500);
}

// Exit Voice Mode
function exitVoiceMode() {
    voiceModeActive = false;
    voiceModeListening = false;

    // Stop recognition
    if (voiceModeRecognition) {
        voiceModeRecognition.abort();
    }

    // Stop any speech
    synthesis.cancel();

    // Hide overlay
    const overlay = document.getElementById('voiceModeOverlay');
    overlay.classList.remove('active');

    // Reset UI
    setVoiceModeAvatar('');
    setVoiceModeStatus('Click to start talking...', '');
    document.getElementById('voiceModeBtn').classList.remove('active');
}

// Initialize Voice Mode Recognition
function initVoiceModeRecognition() {
    if ('webkitSpeechRecognition' in window) {
        voiceModeRecognition = new webkitSpeechRecognition();
    } else if ('SpeechRecognition' in window) {
        voiceModeRecognition = new SpeechRecognition();
    } else {
        setVoiceModeStatus('Speech recognition not supported', 'error');
        return;
    }

    voiceModeRecognition.continuous = false;
    voiceModeRecognition.interimResults = true;
    voiceModeRecognition.lang = 'en-US';

    voiceModeRecognition.onstart = () => {
        voiceModeListening = true;
        document.getElementById('voiceModeBtn').classList.add('active');
        setVoiceModeAvatar('listening');
        setVoiceModeStatus('Listening...', 'listening');
    };

    voiceModeRecognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        // Show transcript
        const transcriptEl = document.getElementById('voiceModeTranscript');
        if (interimTranscript) {
            transcriptEl.textContent = interimTranscript;
            transcriptEl.classList.add('visible');
        }

        if (finalTranscript) {
            transcriptEl.textContent = finalTranscript;

            // Check for exit commands
            const lowerText = finalTranscript.toLowerCase();
            if (lowerText.includes('goodbye') || lowerText.includes('exit') || lowerText.includes('bye')) {
                speakInVoiceMode("Goodbye! It was nice talking to you!");
                setTimeout(() => exitVoiceMode(), 2000);
                return;
            }

            // Process the message
            processVoiceModeMessage(finalTranscript);
        }
    };

    voiceModeRecognition.onerror = (event) => {
        console.error('Voice mode error:', event.error);
        voiceModeListening = false;
        document.getElementById('voiceModeBtn').classList.remove('active');
        setVoiceModeAvatar('');

        if (event.error === 'not-allowed') {
            setVoiceModeStatus('Microphone access denied', 'error');
        } else if (event.error === 'no-speech') {
            setVoiceModeStatus('No speech detected. Click to try again.', '');
        } else if (event.error === 'aborted') {
            // Ignore aborted errors
        } else {
            setVoiceModeStatus('Error: ' + event.error, 'error');
        }
    };

    voiceModeRecognition.onend = () => {
        voiceModeListening = false;
        document.getElementById('voiceModeBtn').classList.remove('active');

        // Only reset avatar if not speaking
        if (!synthesis.speaking) {
            setVoiceModeAvatar('');
        }
    };
}

// Start Voice Mode Listening
function startVoiceModListening() {
    if (!voiceModeActive || !voiceModeRecognition) return;

    try {
        voiceModeRecognition.start();
    } catch (e) {
        console.error('Error starting voice mode:', e);
    }
}

// Toggle Voice Mode Listening
function toggleVoiceModeListening() {
    if (voiceModeListening) {
        voiceModeRecognition.stop();
    } else {
        startVoiceModListening();
    }
}

// Process Voice Mode Message
async function processVoiceModeMessage(message) {
    setVoiceModeStatus('Thinking...', '');
    setVoiceModeAvatar('');

    // Also add to chat history in background
    addMessage('user', message);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.response) {
            // Add to chat
            addMessage('assistant', data.response);

            // Save history
            chatHistory.push({ role: 'user', content: message });
            chatHistory.push({ role: 'assistant', content: data.response });
            saveChatHistory();

            // Speak the response
            speakInVoiceMode(data.response);
        }
    } catch (error) {
        console.error('Error:', error);
        speakInVoiceMode("Sorry, I had trouble understanding. Please try again.");
    }
}

// Speak in Voice Mode
function speakInVoiceMode(text) {
    if (!synthesis) return;

    synthesis.cancel();

    // Clean text
    const cleanText = text
        .replace(/```[\s\S]*?```/g, 'code block')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .replace(/\*([^*]+)\*/g, '$1')
        .replace(/<[^>]*>/g, '')
        .replace(/&[^;]+;/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.1;
    utterance.volume = 1.0;

    // Find a nice voice
    const voices = synthesis.getVoices();
    const femaleVoice = voices.find(v =>
        v.name.includes('Female') ||
        v.name.includes('Samantha') ||
        v.name.includes('Victoria') ||
        v.name.includes('Karen') ||
        v.name.includes('Moira')
    ) || voices.find(v => v.lang.startsWith('en')) || voices[0];

    if (femaleVoice) {
        utterance.voice = femaleVoice;
    }

    utterance.onstart = () => {
        setVoiceModeAvatar('speaking');
        setVoiceModeStatus('Speaking...', 'speaking');
        document.getElementById('voiceModeTranscript').classList.remove('visible');
    };

    utterance.onend = () => {
        setVoiceModeAvatar('');
        setVoiceModeStatus('Click to speak or just start talking...', '');

        // Auto-restart listening after speaking (continuous conversation)
        if (voiceModeActive) {
            setTimeout(() => {
                startVoiceModListening();
            }, 500);
        }
    };

    synthesis.speak(utterance);
}

// Set Voice Mode Avatar State
function setVoiceModeAvatar(state) {
    const avatar = document.getElementById('voiceModeAvatar');
    avatar.classList.remove('listening', 'speaking');
    if (state) {
        avatar.classList.add(state);
    }
}

// Set Voice Mode Status
function setVoiceModeStatus(text, className) {
    const status = document.getElementById('voiceModeStatus');
    status.textContent = text;
    status.className = 'voice-mode-status' + (className ? ' ' + className : '');
}

// ==========================================
// WAKE WORD DETECTION - Like Terminal Version
// ==========================================

// Initialize Wake Word Detection
function initWakeWordDetection() {
    if ('webkitSpeechRecognition' in window) {
        wakeWordRecognition = new webkitSpeechRecognition();
    } else if ('SpeechRecognition' in window) {
        wakeWordRecognition = new SpeechRecognition();
    } else {
        console.warn('Speech recognition not supported');
        return false;
    }

    wakeWordRecognition.continuous = true;
    wakeWordRecognition.interimResults = true;
    wakeWordRecognition.lang = 'en-US';

    wakeWordRecognition.onresult = (event) => {
        if (isProcessingCommand) return;

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript.toLowerCase().trim();

            // Check for wake word
            if (transcript.includes(WAKE_WORD) || transcript.includes("hello katie") ||
                transcript.includes("hey kitty") || transcript.includes("hi kitty")) {
                console.log('🎀 Wake word detected:', transcript);

                if (event.results[i].isFinal) {
                    // Stop wake word listening
                    wakeWordRecognition.stop();

                    // Activate assistant
                    onWakeWordDetected();
                }
            }
        }
    };

    wakeWordRecognition.onerror = (event) => {
        console.error('Wake word error:', event.error);
        if (event.error === 'not-allowed') {
            updateWakeWordStatus('Microphone access denied', 'error');
            wakeWordEnabled = false;
        } else if (event.error !== 'aborted' && event.error !== 'no-speech') {
            // Restart on other errors
            setTimeout(() => {
                if (wakeWordEnabled && !isProcessingCommand) {
                    startWakeWordListening();
                }
            }, 1000);
        }
    };

    wakeWordRecognition.onend = () => {
        // Auto-restart if still enabled and not processing
        if (wakeWordEnabled && !isProcessingCommand) {
            setTimeout(() => {
                startWakeWordListening();
            }, 100);
        }
    };

    return true;
}

// Start Wake Word Listening
function startWakeWordListening() {
    if (!wakeWordRecognition || isProcessingCommand) return;

    try {
        wakeWordRecognition.start();
        updateWakeWordStatus('Listening for "Hello Kitty"...', 'listening');
    } catch (e) {
        // Already started, ignore
    }
}

// Stop Wake Word Listening
function stopWakeWordListening() {
    if (wakeWordRecognition) {
        try {
            wakeWordRecognition.stop();
        } catch (e) {
            // Ignore
        }
    }
}

// Toggle Wake Word Mode - Opens fullscreen interface
function toggleWakeWordMode() {
    if (wakeWordEnabled) {
        exitWakeWordMode();
    } else {
        enterWakeWordMode();
    }
}

// Enter Wake Word Mode with Fullscreen UI
function enterWakeWordMode() {
    wakeWordEnabled = true;

    // Initialize recognition if needed
    if (!wakeWordRecognition) {
        if (!initWakeWordDetection()) {
            wakeWordEnabled = false;
            return;
        }
    }

    // Show overlay
    const overlay = document.getElementById('wakeModeOverlay');
    overlay.classList.add('active');

    // Update UI elements
    updateWakeWordButton(true);
    setWakeModeAvatar('waiting');
    setWakeModeStatus('Say "Hello Kitty" to start...', 'waiting');
    showWakeModeIndicator(true);

    // Start listening
    startWakeWordListening();

    localStorage.setItem('wakeWordEnabled', 'true');
}

// Exit Wake Word Mode
function exitWakeWordMode() {
    wakeWordEnabled = false;
    isProcessingCommand = false;

    // Stop recognition
    stopWakeWordListening();

    // Stop any speech
    synthesis.cancel();

    // Hide overlay
    const overlay = document.getElementById('wakeModeOverlay');
    overlay.classList.remove('active');

    // Reset UI
    updateWakeWordButton(false);
    updateWakeWordStatus('', '');

    localStorage.setItem('wakeWordEnabled', 'false');
}

// Set Wake Mode Avatar State
function setWakeModeAvatar(state) {
    const avatar = document.getElementById('wakeModeAvatar');
    if (avatar) {
        avatar.classList.remove('waiting', 'listening', 'speaking');
        if (state) {
            avatar.classList.add(state);
        }
    }
}

// Set Wake Mode Status
function setWakeModeStatus(text, className) {
    const status = document.getElementById('wakeModeStatus');
    if (status) {
        status.textContent = text;
        status.className = 'wake-mode-status' + (className ? ' ' + className : '');
    }
}

// Show/Hide Wake Mode Indicator
function showWakeModeIndicator(show) {
    const indicator = document.getElementById('wakeModeIndicator');
    if (indicator) {
        if (show) {
            indicator.classList.remove('hidden');
        } else {
            indicator.classList.add('hidden');
        }
    }
}

// Show Wake Mode Transcript
function showWakeModeTranscript(text) {
    const transcript = document.getElementById('wakeModeTranscript');
    if (transcript) {
        transcript.textContent = text;
        transcript.classList.add('visible');
    }
}

// Hide Wake Mode Transcript
function hideWakeModeTranscript() {
    const transcript = document.getElementById('wakeModeTranscript');
    if (transcript) {
        transcript.classList.remove('visible');
    }
}

// On Wake Word Detected
function onWakeWordDetected() {
    isProcessingCommand = true;

    // Update UI
    showWakeModeIndicator(false);
    setWakeModeAvatar('speaking');
    setWakeModeStatus('Yes? How can I help you?', 'speaking');

    // Play acknowledgment
    const utterance = new SpeechSynthesisUtterance("Yes? How can I help you?");
    utterance.rate = 1.0;
    utterance.pitch = 1.1;

    const voices = synthesis.getVoices();
    const femaleVoice = voices.find(v =>
        v.name.includes('Female') || v.name.includes('Samantha') ||
        v.name.includes('Victoria') || v.name.includes('Karen')
    ) || voices.find(v => v.lang.startsWith('en')) || voices[0];

    if (femaleVoice) utterance.voice = femaleVoice;

    utterance.onend = () => {
        listenForCommand();
    };

    synthesis.speak(utterance);
}

// Listen for Command after Wake Word
function listenForCommand() {
    let commandRecognition;

    if ('webkitSpeechRecognition' in window) {
        commandRecognition = new webkitSpeechRecognition();
    } else if ('SpeechRecognition' in window) {
        commandRecognition = new SpeechRecognition();
    } else {
        isProcessingCommand = false;
        if (wakeWordEnabled) startWakeWordListening();
        return;
    }

    commandRecognition.continuous = false;
    commandRecognition.interimResults = true;
    commandRecognition.lang = 'en-US';

    let finalTranscript = '';

    // Update overlay UI
    setWakeModeAvatar('listening');
    setWakeModeStatus('Listening...', 'listening');
    showWakeModeIndicator(true);

    commandRecognition.onresult = (event) => {
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        // Show what user is saying in the overlay transcript
        if (interimTranscript) {
            setWakeModeStatus('Listening...', 'listening');
            showWakeModeTranscript(interimTranscript);
        }
    };

    commandRecognition.onend = () => {
        if (finalTranscript) {
            showWakeModeTranscript(finalTranscript);
            setWakeModeStatus('Processing...', '');
            setWakeModeAvatar('');
            showWakeModeIndicator(false);
            processWakeWordCommand(finalTranscript);
        } else {
            setWakeModeStatus('No command heard. Say "Hello Kitty" to try again...', '');
            setWakeModeAvatar('waiting');
            showWakeModeIndicator(true);
            hideWakeModeTranscript();
            isProcessingCommand = false;
            if (wakeWordEnabled) {
                setTimeout(() => startWakeWordListening(), 500);
            }
        }
    };

    commandRecognition.onerror = (event) => {
        console.error('Command recognition error:', event.error);
        setWakeModeStatus('Error. Say "Hello Kitty" to try again...', 'error');
        setWakeModeAvatar('waiting');
        showWakeModeIndicator(true);
        hideWakeModeTranscript();
        isProcessingCommand = false;
        if (wakeWordEnabled) {
            setTimeout(() => startWakeWordListening(), 500);
        }
    };

    try {
        commandRecognition.start();
    } catch (e) {
        console.error('Error starting command recognition:', e);
        isProcessingCommand = false;
        if (wakeWordEnabled) startWakeWordListening();
    }
}

// Process Command from Wake Word
async function processWakeWordCommand(command) {
    console.log('📝 Command:', command);

    // Check for exit commands
    const lowerCommand = command.toLowerCase();
    if (lowerCommand.includes('goodbye') || lowerCommand.includes('bye') || lowerCommand.includes('exit')) {
        setWakeModeAvatar('speaking');
        setWakeModeStatus('Goodbye!', 'speaking');
        hideWakeModeTranscript();

        const utterance = new SpeechSynthesisUtterance("Goodbye! Have a wonderful day!");
        utterance.rate = 1.0;
        utterance.pitch = 1.1;

        const voices = synthesis.getVoices();
        const femaleVoice = voices.find(v =>
            v.name.includes('Female') || v.name.includes('Samantha') ||
            v.name.includes('Victoria') || v.name.includes('Karen')
        ) || voices.find(v => v.lang.startsWith('en')) || voices[0];
        if (femaleVoice) utterance.voice = femaleVoice;

        utterance.onend = () => {
            exitWakeWordMode();
        };

        synthesis.speak(utterance);
        return;
    }

    // Add to chat UI
    addMessage('user', command);

    // Update overlay to show processing
    setWakeModeAvatar('');
    setWakeModeStatus('Thinking...', '');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: command })
        });

        const data = await response.json();

        if (data.response) {
            addMessage('assistant', data.response);
            chatHistory.push({ role: 'user', content: command });
            chatHistory.push({ role: 'assistant', content: data.response });
            saveChatHistory();

            // Update overlay for speaking
            setWakeModeAvatar('speaking');
            setWakeModeStatus('Speaking...', 'speaking');
            hideWakeModeTranscript();

            // Clean text for speech
            const cleanText = data.response
                .replace(/```[\s\S]*?```/g, 'code block')
                .replace(/`([^`]+)`/g, '$1')
                .replace(/\*\*([^*]+)\*\*/g, '$1')
                .replace(/\*([^*]+)\*/g, '$1')
                .replace(/<[^>]*>/g, '')
                .replace(/&[^;]+;/g, '');

            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            utterance.pitch = 1.1;

            const voices = synthesis.getVoices();
            const femaleVoice = voices.find(v =>
                v.name.includes('Female') || v.name.includes('Samantha') ||
                v.name.includes('Victoria') || v.name.includes('Karen')
            ) || voices.find(v => v.lang.startsWith('en')) || voices[0];

            if (femaleVoice) utterance.voice = femaleVoice;

            utterance.onend = () => {
                isProcessingCommand = false;
                if (wakeWordEnabled) {
                    // Return to waiting state
                    setWakeModeAvatar('waiting');
                    setWakeModeStatus('Say "Hello Kitty" to ask another question...', 'waiting');
                    showWakeModeIndicator(true);
                    startWakeWordListening();
                }
            };

            synthesis.speak(utterance);
        }
    } catch (error) {
        console.error('Error:', error);

        // Show error in overlay
        setWakeModeAvatar('speaking');
        setWakeModeStatus('Sorry, there was an error...', 'error');

        const utterance = new SpeechSynthesisUtterance("Sorry, I had trouble with that. Please try again.");
        utterance.rate = 1.0;
        utterance.pitch = 1.1;

        utterance.onend = () => {
            isProcessingCommand = false;
            if (wakeWordEnabled) {
                setWakeModeAvatar('waiting');
                setWakeModeStatus('Say "Hello Kitty" to try again...', 'waiting');
                showWakeModeIndicator(true);
                setTimeout(() => startWakeWordListening(), 500);
            }
        };

        synthesis.speak(utterance);
    }
}

// Update Wake Word Status Display
function updateWakeWordStatus(text, className) {
    const status = document.getElementById('wakeWordStatus');
    if (status) {
        status.textContent = text;
        status.className = 'wake-word-status' + (className ? ' ' + className : '');
    }
}

// Update Wake Word Button
function updateWakeWordButton(active) {
    const btn = document.getElementById('wakeWordBtn');
    if (btn) {
        if (active) {
            btn.classList.add('active');
            btn.title = 'Wake word active - Click to disable';
        } else {
            btn.classList.remove('active');
            btn.title = 'Enable wake word - Say "Hello Kitty" to activate';
        }
    }
}

// Show Notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'wake-notification';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Auto-enable wake word if previously enabled
document.addEventListener('DOMContentLoaded', () => {
    const wasEnabled = localStorage.getItem('wakeWordEnabled') === 'true';
    if (wasEnabled) {
        setTimeout(() => {
            toggleWakeWordMode();
        }, 1000);
    }
});
