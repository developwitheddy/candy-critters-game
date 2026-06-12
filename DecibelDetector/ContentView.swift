import SwiftUI

struct ContentView: View {
    @StateObject private var monitor = AudioLevelMonitor()

    private var meterColor: Color {
        switch monitor.decibels {
        case ..<40:  return .green
        case ..<70:  return .yellow
        case ..<85:  return .orange
        default:     return .red
        }
    }

    private var label: String {
        switch monitor.decibels {
        case ..<30:  return "Silence"
        case ..<50:  return "Quiet"
        case ..<65:  return "Moderate"
        case ..<80:  return "Loud"
        case ..<90:  return "Very Loud"
        default:     return "Dangerous"
        }
    }

    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()

            VStack(spacing: 36) {

                Text("Decibel Meter")
                    .font(.largeTitle.bold())
                    .foregroundColor(.white)

                // Circular gauge
                ZStack {
                    Circle()
                        .stroke(Color.white.opacity(0.1), lineWidth: 18)

                    Circle()
                        .trim(from: 0, to: CGFloat(monitor.decibels) / 120)
                        .stroke(meterColor, style: StrokeStyle(lineWidth: 18, lineCap: .round))
                        .rotationEffect(.degrees(-90))
                        .animation(.easeOut(duration: 0.05), value: monitor.decibels)

                    VStack(spacing: 4) {
                        Text(monitor.isMonitoring ? "\(Int(monitor.decibels))" : "—")
                            .font(.system(size: 76, weight: .bold, design: .monospaced))
                            .foregroundColor(meterColor)
                            .animation(.none, value: monitor.decibels)
                        Text("dB")
                            .font(.title2.bold())
                            .foregroundColor(.gray)
                        if monitor.isMonitoring {
                            Text(label)
                                .font(.headline)
                                .foregroundColor(meterColor)
                        }
                    }
                }
                .frame(width: 250, height: 250)

                // Bar meter + peak
                if monitor.isMonitoring {
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Text("Level").font(.caption).foregroundColor(.gray)
                            Spacer()
                            Text("Peak: \(Int(monitor.peakDecibels)) dB")
                                .font(.caption).foregroundColor(.orange)
                        }

                        GeometryReader { geo in
                            ZStack(alignment: .leading) {
                                RoundedRectangle(cornerRadius: 4)
                                    .fill(Color.white.opacity(0.1))

                                RoundedRectangle(cornerRadius: 4)
                                    .fill(LinearGradient(
                                        colors: [.green, .yellow, .orange, .red],
                                        startPoint: .leading, endPoint: .trailing
                                    ))
                                    .frame(width: geo.size.width * CGFloat(monitor.decibels) / 120)
                                    .animation(.easeOut(duration: 0.05), value: monitor.decibels)

                                // Peak marker
                                Rectangle()
                                    .fill(Color.white)
                                    .frame(width: 2, height: geo.size.height)
                                    .offset(x: geo.size.width * CGFloat(monitor.peakDecibels) / 120 - 1)
                            }
                        }
                        .frame(height: 22)

                        HStack {
                            ForEach(["0", "30", "60", "90", "120"], id: \.self) { n in
                                Text(n).font(.system(size: 10)).foregroundColor(.gray)
                                if n != "120" { Spacer() }
                            }
                        }
                    }
                    .padding(.horizontal, 24)
                }

                // Start / Stop
                Button {
                    monitor.isMonitoring ? monitor.stopMonitoring() : monitor.startMonitoring()
                } label: {
                    Label(
                        monitor.isMonitoring ? "Stop" : "Start",
                        systemImage: monitor.isMonitoring ? "stop.fill" : "mic.fill"
                    )
                    .font(.title2.bold())
                    .foregroundColor(.black)
                    .frame(width: 170, height: 58)
                    .background(monitor.isMonitoring ? Color.red : Color.green)
                    .clipShape(Capsule())
                }

                if monitor.isMonitoring {
                    Button("Reset Peak") { monitor.resetPeak() }
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }

                Text("Approximate dB SPL — not a calibrated instrument")
                    .font(.caption2)
                    .foregroundColor(Color.white.opacity(0.25))
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
            }
            .padding(.vertical)
        }
    }
}

#Preview {
    ContentView()
}
