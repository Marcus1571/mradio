import Foundation
import AppKit

let clipSymHex: [UInt16] = [0x25CF, 0x25B8, 0x2191, 0x2193, 0x25B2,
                            0x25BC, 0x2588, 0x2591, 0x2014, 0x00B7]

struct Color {
    static let bg = NSColor(red: 5/255.0, green: 7/255.0, blue: 10/255.0, alpha: 1)
    static let headerBg = NSColor(red: 13/255.0, green: 26/255.0, blue: 43/255.0, alpha: 1)
    static let headerBorder = NSColor(red: 27/255.0, green: 51/255.0, blue: 71/255.0, alpha: 1)
    static let cyan = NSColor(red: 88/255.0, green: 166/255.0, blue: 255/255.0, alpha: 1)
    static let station = NSColor(red: 0.788, green: 0.906, blue: 1, alpha: 1)
    static let dim = NSColor(red: 0.490, green: 0.576, blue: 0.659, alpha: 1)
    static let composer = NSColor(red: 0.604, green: 0.655, blue: 0.710, alpha: 1)
    static let title = Color.cyan
    static let desc = NSColor(red: 0.714, green: 0.761, blue: 0.812, alpha: 1)
    static let streamLine = NSColor(red: 0.373, green: 0.427, blue: 0.478, alpha: 1)
    static let liveText = NSColor(red: 63/255.0, green: 185/255.0, blue: 80/255.0, alpha: 1)
    static let volLabel = Color.dim
    static let footerTop = NSColor(red: 0.224, green: 0.325, blue: 0.420, alpha: 1)
    static let footerMid = NSColor(red: 0.192, green: 0.251, blue: 0.302, alpha: 1)
    static let footerBot = NSColor(red: 0.129, green: 0.165, blue: 0.200, alpha: 1)
}

func f(_ name: String, _ size: CGFloat) -> NSFont {
    (NSFont(name: name, size: size) ?? NSFont.monospacedSystemFont(ofSize: size, weight: .regular))
}

struct Shot {
    var rep: NSBitmapImageRep
    var ctx: CGContext
    var y: CGFloat
    let w: CGFloat

    init(_ width: CGFloat, _ height: CGFloat) {
        w = width
        rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(width),
                               pixelsHigh: Int(height), bitsPerSample: 8,
                               samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                               colorSpaceName: .deviceRGB, bytesPerRow: 0,
                               bitsPerPixel: 0)!
        ctx = NSGraphicsContext(bitmapImageRep: rep)!.cgContext
        ctx.setFillColor(Color.bg.cgColor)
        ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
        ctx.translateBy(x: 0, y: height)
        ctx.scaleBy(x: 1, y: -1)
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
        y = 0
    }

    mutating func lineGap(_ g: CGFloat) { y += g }

    mutating func draw(_ s: String, x: CGFloat = 0, size: CGFloat = 20,
                       color: NSColor, bold: Bool = false) {
        let font = f(bold ? "Menlo-Bold" : "Menlo", size)
        let attrs: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: color]
        (s as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs)
        y += size * 1.24
    }

    mutating func rule() {
        ctx.setFillColor(Color.headerBorder.cgColor)
        ctx.fill(CGRect(x: 0, y: y, width: w, height: 1))
        lineGap(4)
    }

    mutating func header(_ title: String, live: Bool = false) {
        ctx.setFillColor(Color.headerBg.cgColor)
        ctx.fill(CGRect(x: 0, y: y, width: w, height: 62))
        y += 18
        var x: CGFloat = 20
        let h = 24.0
        let attrs = { (sz: CGFloat, c: NSColor, bold: Bool) -> [NSAttributedString.Key: Any] in
            [.font: f(bold ? "Menlo-Bold" : "Menlo", sz), .foregroundColor: c]
        }
        ("\u{25CF} RADIO" as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs(h + 2, Color.cyan, true))
        x += ("\u{25CF} RADIO" as NSString).size(withAttributes: attrs(h + 2, .white, true)).width + 14
        ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs(h, Color.dim, false))
        x += 24
        (title as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs(h - 1, Color.station, false))
        x += (title as NSString).size(withAttributes: attrs(h - 1, .white, false)).width + 14
        ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs(h, Color.dim, false))
        x += 26
        let pillW: CGFloat = 64, pillH: CGFloat = 30
        ctx.setStrokeColor(Color.liveText.cgColor)
        ctx.setFillColor(NSColor(red: 22/255.0, green: 55/255.0, blue: 31/255.0, alpha: 1).cgColor)
        let rect = CGRect(x: x, y: y - 4, width: pillW, height: pillH)
        ctx.addPath(CGPath(roundedRect: rect, cornerWidth: pillH / 2, cornerHeight: pillH / 2, transform: nil))
        ctx.fillPath()
        ctx.addPath(CGPath(roundedRect: rect, cornerWidth: pillH / 2, cornerHeight: pillH / 2, transform: nil))
        ctx.strokePath()
        ("LIVE" as NSString).draw(at: NSPoint(x: x + 15, y: y + 3), withAttributes: attrs(h - 4, Color.liveText, true))
        y += 62
        rule()
    }

    mutating func footer(keys: [[NSAttributedString]], sizes: [CGFloat]) {
        ctx.setFillColor(NSColor(red: 6/255.0, green: 8/255.0, blue: 11/255.0, alpha: 1).cgColor)
        ctx.fill(CGRect(x: 0, y: y, width: w, height: 122))
        y += 14
        for (i, line) in keys.enumerated() {
            var x: CGFloat = 20
            for part in line {
                (part.string as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: part.attributes(at: 0, effectiveRange: nil))
                x += (part.string as NSString).size(withAttributes: part.attributes(at: 0, effectiveRange: nil)).width
            }
            y += sizes[i]
        }
    }
}

func r(_ s: String, _ c: NSColor, _ sz: CGFloat, _ bold: Bool = false) -> NSAttributedString {
    NSAttributedString(string: s, attributes: [.font: f(bold ? "Menlo-Bold" : "Menlo", sz), .foregroundColor: c])
}

func wrap(_ s: String, width: CGFloat, size: CGFloat) -> [NSAttributedString] {
    let words = s.components(separatedBy: " ")
    var lines: [NSAttributedString] = []
    var cur = ""
    let font = f("Menlo", size)
    func widthOf(_ t: String) -> CGFloat { (t as NSString).size(withAttributes: [.font: font]).width }
    for w in words {
        let cand = cur.isEmpty ? w : cur + " " + w
        if widthOf(cand) <= width { cur = cand } else {
            if !cur.isEmpty { lines.append(NSAttributedString(string: cur)) }
            cur = w
        }
    }
    if !cur.isEmpty { lines.append(NSAttributedString(string: cur)) }
    return lines.map { NSAttributedString(string: $0.string,
        attributes: [.font: font, .foregroundColor: Color.desc]) }
}

enum Scene { case player, favorites, all }

let scene: Scene = CommandLine.arguments.count > 1 && CommandLine.arguments[1] == "fav" ? .favorites
                  : CommandLine.arguments[1] == "all" ? .all : .player
let out = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "/tmp/shot.png"

let W: CGFloat = 1500
let hdr: CGFloat = 92
let foot: CGFloat = 150

var sh: Shot
let body = 20.0

switch scene {
case .player:
    sh = Shot(W, 860)
    sh.header("VCR Auditorium | Venice Classic Radio Italia", live: true)
    sh.y += 22
    sh.draw("Johannes Brahms (1833-1897)", size: body, color: Color.composer)
    sh.draw("Sinfonia in do minore No.1 Op.68", size: body + 8, color: Color.title, bold: true)
    sh.draw("(Chicago Symphony Orchestra - Sir Georg Solti, direttore)", size: body, color: Color.composer)
    sh.lineGap(8)
    let desc = "Johannes Brahms (1833-1897), a German composer bridging Classicism and Romanticism, took over two decades to write his four-movement Symphony No. 1 in C minor, premiering it in Karlsruhe in November 1876. Hans von Bülow called it 'Beethoven's Tenth.' The finale's horn-and-violin motto evokes an Alphorn tune he once described."
    let dl = wrap(desc, width: 1100, size: body - 2)
    for l in dl { sh.draw(l.string, size: body - 2, color: Color.desc) }
    sh.lineGap(14)
    sh.draw("\u{2014} \u{00B7} 48 kHz \u{00B7} mp3 \u{00B7} cache \u{2014} \u{00B7} stream 03:47 \u{00B7} o:open article", size: body - 4, color: Color.streamLine)
    sh.lineGap(6)
    ("vol " as NSString).draw(at: NSPoint(x: 40, y: sh.y), withAttributes: [.font: f("Menlo", body - 2), .foregroundColor: Color.volLabel])
    let on = 40, off = 16
    let bar = String(repeating: "\u{2588}", count: on) + String(repeating: "\u{2591}", count: off)
    let green: [NSAttributedString.Key: Any] = [.font: f("Menlo", body - 2), .foregroundColor: Color.liveText]
    let grey:  [NSAttributedString.Key: Any] = [.font: f("Menlo", body - 2), .foregroundColor: Color.streamLine]
    var x: CGFloat = 40 + 42
    for i in 0..<on { (String(bar[bar.index(bar.startIndex, offsetBy: i)]) as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: i < on ? green : grey); x += 14.0 }
    for i in on..<bar.count { (String(bar[bar.index(bar.startIndex, offsetBy: i)]) as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: grey); x += 14.0 }
    ("70%" as NSString).draw(at: NSPoint(x: x + 16, y: sh.y), withAttributes: [.font: f("Menlo", body - 2), .foregroundColor: Color.streamLine])
    sh.y += body
    sh.lineGap(12)
    sh.footer(keys: [
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 18), r("   now:", Color.footerTop, 17), r("opencode", Color.footerMid, 17, true), r("   press to re-request   ", Color.footerTop, 17), r("z:expand", Color.cyan, 18)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 17)],
        [r("q:quit   space:pause   + / -:volume   m:mute   r:reconnect   o:open article", Color.footerBot, 17), r("   v0.7.35", Color.dim, 17)]
    ], sizes: [26, 24, 24])
case .favorites:
    sh = Shot(W, 820)
    sh.header("favorites")
    sh.y += 16
    sh.draw("\u{2014} Enter picks, a adds this row to my list, Esc back", size: body - 3, color: Color.title, bold: true)
    sh.lineGap(10)
    let items = ["VCR Auditorium | Venice Classic Radio Italia", "VCR Classica+ | Venice Classic Radio Italia", "Radio Swiss Classic", "Naim Classical", "WQXR", "Classic FM", "Swiss Jazz", "Radio Paradise", "radio klassik Stephansdom", "NPO Klassiek", "France Musique", "BBC Radio 3"]
    for (i, it) in items.enumerated() {
        let cursor = i == 0
        let tag = i < 9 ? "  \(i + 1)." : i == 9 ? "  0." : "     "
        var x: CGFloat = 40
        if cursor {
            ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f("Menlo-Bold", body), .foregroundColor: Color.liveText])
            x += 22
        }
        let hot = i < 10
        let col: NSColor = cursor ? Color.liveText : (hot ? Color.composer : Color.streamLine)
        (tag as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f(hot ? "Menlo" : "Menlo", body), .foregroundColor: col])
        x += (hot ? 84 : 34)
        (it as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f(cursor ? "Menlo-Bold" : "Menlo", body), .foregroundColor: cursor ? Color.station : col])
        sh.y += body * 1.22
        if i == 0 { sh.y += 2 }
    }
    sh.footer(keys: [
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 18), r("   now:", Color.footerTop, 17), r("opencode", Color.footerMid, 17, true), r("   press to re-request   ", Color.footerTop, 17), r("z:expand", Color.cyan, 18)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 17)],
        [r("Enter:pick   \u{2191}/\u{2193}:move   a:add   q/Esc:back", Color.footerBot, 17), r("   v0.7.35", Color.dim, 17)]
    ], sizes: [26, 24, 24])
case .all:
    sh = Shot(W, 800)
    sh.header("all stations")
    sh.y += 16
    sh.draw("\u{2014} Enter picks, a adds this row to my list, Esc back", size: body - 3, color: Color.title, bold: true)
    sh.lineGap(10)
    let items = ["VCR Auditorium", "VCR Classica+", "Radio Swiss Classic", "Naim Classical", "WQXR", "Classic FM", "Swiss Jazz", "Radio Paradise", "radio klassik Stephansdom", "NPO Radio 4 / Klassiek"]
    for (i, it) in items.enumerated() {
        let cursor = i == 0
        let tag = String(format: "S%02d", i + 1)
        var x: CGFloat = 40
        if cursor {
            ("\u{25B8}" as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f("Menlo-Bold", body), .foregroundColor: Color.liveText])
            x += 22
        }
        let col: NSColor = cursor ? Color.liveText : Color.composer
        (tag as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f("Menlo", body), .foregroundColor: col])
        x += 64
        (it as NSString).draw(at: NSPoint(x: x, y: sh.y), withAttributes: [.font: f(cursor ? "Menlo-Bold" : "Menlo", body), .foregroundColor: cursor ? Color.station : col])
        sh.y += body * 1.22
        if i == 0 { sh.y += 2 }
    }
    sh.lineGap(2)
    sh.draw("\u{2193} more\u{2026}", size: body - 3, color: Color.streamLine)
    sh.footer(keys: [
        [r("AI: 1=opencode 2=ollama 3=api", Color.footerTop, 18), r("   now:", Color.footerTop, 17), r("opencode", Color.footerMid, 17, true), r("   press to re-request   ", Color.footerTop, 17), r("z:expand", Color.cyan, 18)],
        [r("f:favorites   s:all   k:kb   v:check", Color.footerMid, 17)],
        [r("Enter:pick   f:fav   \u{2191}/\u{2193}:move   q/Esc:back   v:check", Color.footerBot, 17), r("   v0.7.35", Color.dim, 17)]
    ], sizes: [26, 24, 24])
}

let png = sh.rep.representation(using: .png, properties: [:])!
try! png.write(to: URL(fileURLWithPath: out))
print("wrote", out)