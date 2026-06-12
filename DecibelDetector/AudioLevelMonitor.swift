import AVFoundation
import Combine

class AudioLevelMonitor: ObservableObject {
    @Published var decibels: Float = 0
    @Published var peakDecibels: Float = 0
    @Published var isMonitoring = false

    private var audioRecorder: AVAudioRecorder?
    private var timer: Timer?

    func startMonitoring() {
        AVAudioSession.sharedInstance().requestRecordPermission { [weak self] granted in
            guard granted else { return }
            DispatchQueue.main.async { self?.setupRecorder() }
        }
    }

    private func setupRecorder() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.record, mode: .measurement, options: [])
            try session.setActive(true)

            let settings: [String: Any] = [
                AVFormatIDKey: Int(kAudioFormatAppleLossless),
                AVSampleRateKey: 44100.0,
                AVNumberOfChannelsKey: 1,
                AVEncoderAudioQualityKey: AVAudioQuality.min.rawValue
            ]

            audioRecorder = try AVAudioRecorder(url: URL(fileURLWithPath: "/dev/null"), settings: settings)
            audioRecorder?.isMeteringEnabled = true
            audioRecorder?.record()

            isMonitoring = true
            peakDecibels = 0

            timer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
                self?.tick()
            }
        } catch {
            print("Audio setup error: \(error)")
        }
    }

    func stopMonitoring() {
        timer?.invalidate()
        timer = nil
        audioRecorder?.stop()
        audioRecorder = nil
        isMonitoring = false
        decibels = 0
        try? AVAudioSession.sharedInstance().setActive(false)
    }

    func resetPeak() {
        peakDecibels = decibels
    }

    private func tick() {
        audioRecorder?.updateMeters()
        // averagePower returns dBFS (-160…0); add ~90 for approximate dB SPL
        let raw = audioRecorder?.averagePower(forChannel: 0) ?? -160
        let mapped = max(0, min(120, raw + 90))
        decibels = mapped
        if mapped > peakDecibels { peakDecibels = mapped }
    }
}
