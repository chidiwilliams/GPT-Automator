//
//  ContentView.swift
//  Fizz
//
//  Created by Chidi Williams on 11/02/2023.
//

import SwiftUI
import AVFoundation
import whisper

enum WhisperModel: String {
    case tiny
}

func getModelPath(model: WhisperModel) -> URL {
    return FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask).first!.appending(path: "Buzz").appending(path: "ggml-model-whisper-\(model.rawValue).bin")
}

struct ContentView: View {
    @State var recorder: AudioRecorder?
    @State private var buffer: [Float] = []
    @State private var isRecording = false
    var queue = DispatchQueue(label: "transcription", qos: DispatchQoS(qosClass: .userInitiated, relativePriority: 0))
    
    var body: some View {
        VStack {
            Button(isRecording ? "Stop" : "Record") {
                if isRecording {
                    recorder?.pause()
                    isRecording = false
                    
                    queue.async {
                        let modelPath = getModelPath(model: .tiny)
                        let ctx = whisper_init_from_file(modelPath.path(percentEncoded: false))
                        
                        var params: whisper_full_params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY)
                        params.print_realtime   = true
                        params.print_progress   = false
                        params.print_timestamps = false
                        params.print_special    = false
                        params.translate        = false
                        params.language         = NSString(string: "en").utf8String
                        params.n_threads        = 4
                        params.offset_ms        = 0
                        
                        let returnCode = whisper_full(ctx, params, &buffer, Int32(buffer.count))
                        if returnCode != 0 {
                            print("whisper model return code \(returnCode), skipping...")
                            return
                        }
                        
                        var text = ""
                        
                        let n_segments = whisper_full_n_segments(ctx)
                        for i in 0..<n_segments {
                            if let segment_text = whisper_full_get_segment_text(ctx, i) {
                                if let ns_string = NSString(utf8String: segment_text) {
                                    text += String(ns_string)
                                }
                            }
                        }
                        
                        text = text.trimmingCharacters(in: CharacterSet.whitespaces)
                        
                        print(text)
                    }
                } else {
                    buffer = []
                    recorder = AudioRecorder(microphoneUniqueID: AVCaptureDevice.default(for: .audio)?.uniqueID)
                    recorder?.record(callback: { samples, sampleCount in
                        self.buffer.append(contentsOf: UnsafeBufferPointer(start: samples, count: sampleCount))
                    })
                    
                    isRecording = true
                }
            }
        }
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
