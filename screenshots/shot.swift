import Foundation
import AppKit

enum Scene { case player, favorites, all }

struct Color {
    static let bg = NSColor(red: 5/255.0, green: 7/255.0, blue: 10/255.0, alpha: 1)
    static let headerBg = NSColor(red: 13/255.0, green: 26/255.0, blue: 43/255.0, alpha: 1)
    static let headerBorder = NSColor(red: 27/255.0, green: 51/255.0, blue: 71/255.0, alpha: 1)
    static let cyan = NSColor(red: 88/255.0, green: 166/255.0, blue: 255/255.0, alpha: 1)
    static let station = NSColor(red: 0.788, green: 0.906, blue: 1, alpha: 1)
    static let dim = NSColor(red: 0.490, green: 0.576, blue: 0.659, alpha: 1)
    static let composer = NSColor(red: 0.604, green: 0.655, blue: 0.710, alpha: 1)
    static let desc = NSColor(red: 0.714, green: 0.761, blue: 0.812, alpha: 1)
    static let streamLine = NSColor(red: 0.373, green: 0.427, blue: 0.478, alpha: 1)
    static let liveText = NSColor(red: 63/255.0, green: 185/255.0, blue: 80/255.0, alpha: 1)
    static let footerTop = NSColor(red: 0.224, green: 0.325, blue: 0.420, alpha: 1)
    static let footerMid = NSColor(red: 0.192, green: 0.251, blue: 0.302, alpha: 1)
    static let footerBot = NSColor(red: 0.129, green: 0.165, blue: 0.200, alpha: 1)
}

func f(_ name: String, _ size: CGFloat) -> NSFont {
    (NSFont(name: name, size: size) ?? NSFont.monospacedSystemFont(ofSize: size, weight: .regular))
}

func attrs(_ size: CGFloat, _ color: NSColor, _ bold: Bool = false) -> [NSAttributedString.Key: Any] {
    [.font: f(bold ? "Menlo-Bold" : "Menlo", size), .foregroundColor: color]
}

func w(_ s: String, _ a: [NSAttributedString.Key: Any]) -> CGFloat {
    (s as NSString).size(withAttributes: a).width
}

final class Shot {
    let W: CGFloat
    let H: CGFloat
    let rep: NSBitmapImageRep
    let ctx: CGContext
    var top: CGFloat = 0

    init(_ width: CGFloat, _ height: CGFloat) {
        W = width; H = height
        rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(width),
                               pixelsHigh: Int(height), bitsPerSample: 8,
                               samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                               colorSpaceName: .deviceRGB, bytesPerRow: 0,
                               bitsPerPixel: 0)!
        ctx = NSGraphicsContext(bitmapImageRep: rep)!.cgContext   // unflipped: y=0 at bottom
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
        ctx.setFillColor(Color.bg.cgColor)
        ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    }

    private func originY(_ size: CGFloat) -> CGFloat {
        H - top - size * 1.24          // origin = lower-left of text frame
    }

    func fill(_ yTop: CGFloat, _ h: CGFloat, _ color: NSColor) {
        ctx.setFillColor(color.cgColor)
        ctx.fill(CGRect(x: 0, y: H - yTop - h, width: W, height: h))
    }

    func line(_ s: String, _ size: CGFloat, _ color: NSColor, _ bold: Bool = false,
              x: CGFloat = 24, topInset: CGFloat = 0) {
        (s as NSString).draw(at: NSPoint(x: x, y: originY(size) - topInset),
                             withAttributes: attrs(size, color, bold))
        top += size * 1.24 + topInset
    }

    func gap(_ g: CGFloat) { top += g }

    func rule() {
        ctx.setFillColor(Color.headerBorder.cgColor)
        ctx.fill(CGRect(x: 0, y: H - top, width: W, height: 1))
        top += 5
    }

    func header(_ title: String, live: Bool = false) {
        let Hbar: CGFloat = 62
        fill(0, Hbar, Color.headerBg)
        let sy = H - top - 26
        var x: CGFloat = 20
        let a = attrs(22, Color.cyan, true)
        ("\u{25CF} RADIO" as NSString).draw(at: NSPoint(x: x, y: sy), withAttributes: a)
        x += w("\u{25CF} RADIO", a) + 12
        ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sy), withAttributes: attrs(20, Color.dim))
        x += 22
        (title as NSString).draw(at: NSPoint(x: x, y: sy), withAttributes: attrs(21, Color.station))
        x += w(title, attrs(21, Color.station)) + 12
        ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sy), withAttributes: attrs(20, Color.dim))
        x += 24
        if live {
            let rect = CGRect(x: x, y: sy - 6, width: 62, height: 30)
            ctx.setStrokeColor(Color.liveText.cgColor)
            ctx.setFillColor(NSColor(red: 22/255.0, green: 55/255.0, blue: 31/255.0, alpha: 1).cgColor)
            ctx.addPath(CGPath(roundedRect: rect, cornerWidth: 15, cornerHeight: 15, transform: nil))
            ctx.fillPath()
            ctx.addPath(CGPath(roundedRect: rect, cornerWidth: 15, cornerHeight: 15, transform: nil))
            ctx.strokePath()
            ("LIVE" as NSString).draw(at: NSPoint(x: x + 14, y: sy + 4), withAttributes: attrs(17, Color.liveText, true))
        }
        top += Hbar
        rule()
    }

    func footer(_ rows: [[NSAttributedString]], pitch: CGFloat = 25) {
        fill(top, H - top, NSColor(red: 6/255.0, green: 8/255.0, blue: 11/255.0, alpha: 1))
        top += 14
        for row in rows {
            var x: CGFloat = 20
            for part in row {
                let sa = part.attributes(at: 0, effectiveRange: nil)
                (part.string as NSString).draw(at: NSPoint(x: x, y: originY(0) ), withAttributes: sa)
                x += w(part.string, sa)
            }
            top += pitch
        }
    }
}

func r(_ s: String, _ c: NSColor, _ sz: CGFloat, _ bold: Bool = false) -> NSAttributedString {
    NSAttributedString(string: s, attributes: attrs(sz, c, bold))
}

func wrappedLines(_ s: String, width: CGFloat, size: CGFloat, color: NSColor) -> [String] {
    let words = s.components(separatedBy: " ")
    var lines: [String] = []
    var cur = ""
    for word in words {
        let cand = cur.isEmpty ? word : cur + " " + word
        if w(cand, attrs(size, color)) <= width { cur = cand } else {
            if !cur.isEmpty { lines.append(cur) }
            cur = word
        }
    }
    if !cur.isEmpty { lines.append(cur) }
    return lines
}

let scene: Scene = CommandLine.arguments.count > 1 && CommandLine.arguments[1] == "fav" ? .favorites
                  : CommandLine.arguments[1] == "all" ? .all : .player
let out = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "/tmp/shot.png"
let body = 20.0, W: CGFloat = 1500

switch scene {
case .player:
    let sh = Shot(W, 490)
    sh.header("VCR Auditorium | Venice Classic Radio Italia", live: true)
    sh.top += 20
    sh.line("Johannes Brahms (1833-1897)", body, Color.composer)
    sh.line("Sinfonia in do minore No.1 Op.68", body + 8, Color.cyan, true)
    sh.line("(Chicago Symphony Orchestra - Sir Georg Solti, direttore)", body, Color.composer)
    sh.top += 8
    let desc = "Johannes Brahms (1833-1897), a German composer bridging Classicism and Romanticism, took over two decades to write his four-movement Symphony No. 1 in C minor, premiering it in Karlsruhe in November 1876. Hans von Bülow called it 'Beethoven's Tenth.' The finale's horn-and-violin motto evokes an Alphorn tune he once described."
    for dl in wrappedLines(desc, width: 1100, size: body - 2, color: Color.desc) {
        sh.line(dl, body - 2, Color.desc)
    }
    sh.top += 12
    sh.line("\u{2014} \u{00B7} 48 kHz \u{00B7} mp3 \u{00B7} cache \u{2014} \u{00B7} stream 03:47 \u{00B7} o:open article", body - 4, Color.streamLine)
    sh.top += 10
    let sy = sh.top
    let lh = (body - 2) * 1.24
    ("vol " as NSString).draw(at: NSPoint(x: 40, y: sh.H - sy - lh), withAttributes: attrs(body - 2, Color.dim))
    var x: CGFloat = 40 + 42
    let green = attrs(body - 2, Color.liveText)
    let grey = attrs(body - 2, Color.streamLine)
    for i in 0..<40 { ("\u{2588}" as NSString).draw(at: NSPoint(x: x, y: sh.H - sy - lh), withAttributes: i < 40 ? green : grey); x += 13 }
    for _ in 0..<16  { ("\u{2591}" as NSString).draw(at: NSPoint(x: x, y: sh.H - sy - lh), withAttributes: grey); x += 13 }
    ("70%" as NSString).draw(at: NSPoint(x: x + 14, y: sh.H - sy - lh), withAttributes: grey)
    sh.top += lh + 10
    sh.footer([
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 17), r("   now:", Color.footerTop, 16), r("opencode", Color.footerMid, 16, true), r("   press to re-request   ", Color.footerTop, 16), r("z:expand", Color.cyan, 17)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 16)],
        [r("q:quit   space:pause   + / -:volume   m:mute   r:reconnect   o:open article", Color.footerBot, 16), r("   v0.7.36", Color.dim, 16)]
    ])
    save(sh, out)

case .favorites:
    let sh = Shot(W, 520)
    sh.header("favorites")
    sh.top += 14
    sh.line("\u{2014} Enter picks, a adds this row to my list, Esc back", body - 3, Color.cyan, true)
    sh.top += 8
    let items = ["VCR Auditorium | Venice Classic Radio Italia", "VCR Classica+ | Venice Classic Radio Italia", "Radio Swiss Classic", "Naim Classical", "WQXR", "Classic FM", "Swiss Jazz", "Radio Paradise", "radio klassik Stephansdom", "NPO Klassiek", "France Musique", "BBC Radio 3"]
    for (i, it) in items.enumerated() {
        let cursor = i == 0
        let tag = i < 9 ? "\(i + 1)." : i == 9 ? "0." : "  "
        var x: CGFloat = 40
        let a = attrs(body, Color.composer)
        if cursor {
            ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24), withAttributes: attrs(body, Color.liveText, true))
            x += 22
        }
        (tag as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24), withAttributes: a)
        x += cursor ? 80 : (i < 10 ? 34 : 34)
        (it as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24),
                              withAttributes: attrs(body, cursor ? Color.station : Color.composer, cursor))
        sh.top += body * 1.24
    }
    sh.footer([
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 17), r("   now:", Color.footerTop, 16), r("opencode", Color.footerMid, 16, true), r("   press to re-request   ", Color.footerTop, 16), r("z:expand", Color.cyan, 17)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 16)],
        [r("Enter:pick   \u{2191}/\u{2193}:move   a:add   q/Esc:back", Color.footerBot, 16), r("   v0.7.36", Color.dim, 16)]
    ])
    save(sh, out)

case .all:
    let sh = Shot(W, 495)
    sh.header("all stations")
    sh.top += 14
    sh.line("\u{2014} Enter picks, a adds this row to my list, Esc back", body - 3, Color.cyan, true)
    sh.top += 8
    let items = ["VCR Auditorium", "VCR Classica+", "Radio Swiss Classic", "Naim Classical", "WQXR", "Classic FM", "Swiss Jazz", "Radio Paradise", "radio klassik Stephansdom", "NPO Radio 4 / Klassiek"]
    for (i, it) in items.enumerated() {
        let cursor = i == 0
        let tag = String(format: "S%02d", i + 1)
        var x: CGFloat = 40
        let a = attrs(body, Color.composer)
        if cursor {
            ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24), withAttributes: attrs(body, Color.liveText, true))
            x += 22
        }
        (tag as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24), withAttributes: a)
        x += 62
        (it as NSString).draw(at: NSPoint(x: x, y: sh.H - sh.top - body * 1.24),
                              withAttributes: attrs(body, cursor ? Color.station : Color.composer, cursor))
        sh.top += body * 1.24
    }
    sh.top += 2
    sh.line("\u{2193} more\u{2026}", body - 3, Color.streamLine)
    sh.footer([
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 17), r("   now:", Color.footerTop, 16), r("opencode", Color.footerMid, 16, true), r("   press to re-request   ", Color.footerTop, 16), r("z:expand", Color.cyan, 17)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 16)],
        [r("Enter:pick   f:fav   \u{2191}/\u{2193}:move   q/Esc:back   v:check", Color.footerBot, 16), r("   v0.7.36", Color.dim, 16)]
    ])
    save(sh, out)
}

func save(_ sh: Shot, _ path: String) {
    let data = sh.rep.representation(using: .png, properties: [:])!
    try! data.write(to: URL(fileURLWithPath: path))
    print("wrote", path)
}