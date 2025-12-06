// Sound effects for Tic-Tac-Toe game
class GameSounds {
    constructor() {
        this.audioContext = null;
        this.enabled = true;
        this.initAudio();
    }

    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API not supported');
        }
    }

    // Create a simple beep sound
    createBeep(frequency, duration, type = 'sine') {
        if (!this.audioContext || !this.enabled) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
        oscillator.type = type;

        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    // Sound for player move
    playMove() {
        this.createBeep(800, 0.15, 'square');
    }

    // Sound for AI move
    playAIMove() {
        this.createBeep(600, 0.2, 'sawtooth');
    }

    // Sound for win
    playWin() {
        // Play a victory melody
        setTimeout(() => this.createBeep(523, 0.2), 0);   // C
        setTimeout(() => this.createBeep(659, 0.2), 150); // E
        setTimeout(() => this.createBeep(784, 0.3), 300); // G
    }

    // Sound for loss
    playLoss() {
        // Play a descending tone
        setTimeout(() => this.createBeep(400, 0.3), 0);
        setTimeout(() => this.createBeep(300, 0.3), 200);
        setTimeout(() => this.createBeep(200, 0.4), 400);
    }

    // Sound for draw
    playDraw() {
        // Play neutral tones
        setTimeout(() => this.createBeep(440, 0.15), 0);  // A
        setTimeout(() => this.createBeep(440, 0.15), 200); // A
        setTimeout(() => this.createBeep(440, 0.15), 400); // A
    }

    // Sound for reset/new game
    playReset() {
        this.createBeep(1000, 0.1, 'triangle');
    }

    // Toggle sound on/off
    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }
}

// Create global sound instance
const gameSounds = new GameSounds();
