"""Build training illustrations from the experiment report, not an audited run config.

Run from the repository root: python3 scripts/build_finetuning_figures.py
The timestamps, frames and probability bars are illustrative. No private media.
"""
from build_architecture_figures import SVG, OUT


def pill(s, x, y, w, label, color="green", size=17):
    s.rect(x, y, w, 34, fill="bg", stroke=color, r=7)
    s.text(x+w/2, y+23, label, size, color, 700, "middle")


def label_data(mobile=False):
    s = SVG(540 if mobile else 1320, 1820 if mobile else 1040,
            "How CCTV annotations become training examples",
            "Illustration of the reported label rule. The original dataset contains video and XML event type, start time and duration, rather than written question-answer pairs. A hypothetical falling event from 20 to 30 seconds gives normal labels at 15 and 35 seconds and a falling label at 25 seconds. Fixed anomaly and event questions are paired with frames and XML-derived targets. These are conceptual examples, not exported training records. The reported L3 result uses one frame per decision and only falling and abandoned-object event data.")
    s.header("04", "Where training labels come from", mobile)
    s.text(32, 112, "Video + event times → frame + question + answer", 18 if mobile else 21, "muted")
    if mobile:
        s.rect(28, 144, 484, 182, stroke="blue")
        s.label(48, 182, "1", "Original CCTV data")
        s.frame(48, 208, 122, 82)
        s.text(196, 237, "Video + XML", 27, weight=700)
        s.text(196, 271, "No written Q&A", 20, "muted")
        s.rect(28, 350, 484, 150, stroke="purple")
        s.text(48, 385, "ILLUSTRATIVE XML ANNOTATION", 14, "purple", 700)
        s.text(48, 427, "Event: falling", 27, "purple", 700)
        s.text(48, 469, "Start 20 s  ·  Duration 10 s", 23)
        s.line(270, 504, 270, 536, "purple", arrow=True)
        tx, ty, tw = 28, 550, 484
    else:
        s.rect(32, 146, 576, 170, stroke="blue")
        s.label(56, 184, "1", "Original CCTV data")
        s.frame(56, 205, 140, 88)
        s.text(224, 240, "Video + XML annotation", 27, weight=700)
        s.text(224, 278, "No written question–answer pairs", 20, "muted")
        s.rect(648, 146, 640, 170, stroke="purple")
        s.text(672, 182, "ILLUSTRATIVE XML ANNOTATION", 14, "purple", 700)
        s.text(672, 229, "Event: falling", 30, "purple", 700)
        s.text(672, 274, "Start 20 s  ·  Duration 10 s", 24)
        s.path("M320 318 V337 H660 V354", "blue", arrow=True)
        s.path("M968 318 V337 H660", "purple")
        tx, ty, tw = 32, 368, 1256

    # A real time axis: samples at 15, 25 and 35 s, event between 20 and 30 s.
    s.rect(tx, ty, tw, 226, stroke="line")
    s.label(tx+20, ty+37, "2", "Map each frame to its time")
    ax, aw, ay = tx+44, tw-88, ty+100
    s.rect(ax, ay-10, aw, 20, fill="line", stroke="none", r=6)
    s.rect(ax+aw/3, ay-10, aw/3, 20, fill="purple", stroke="none", r=5)
    s.text(ax+aw/2, ay-28, "falling", 19, "purple", 700, "middle")
    for sec in (10, 20, 30, 40):
        x = ax+(sec-10)/30*aw
        s.line(x, ay+14, x, ay+25, "muted", width=1)
        s.text(x, ay+48, f"{sec} s", 17, "muted", anchor="middle")
    for sec in (15, 25, 35):
        x = ax+(sec-10)/30*aw
        s.circle(x, ay, 6, "orange" if sec==25 else "blue")
        s.line(x, ay+62, x, ay+81, "orange" if sec==25 else "blue", arrow=True)
        s.text(x, ay+106, f"{sec} s", 20, "orange" if sec==25 else "blue", 700, "middle")

    if mobile:
        sy = 820
        s.label(48, sy, "3", "Add the two fixed questions", "green")
        cards = [(28, 844+i*234, 484, sec) for i, sec in enumerate((15, 25, 35))]
        for x, y, w, sec in cards:
            positive = sec==25
            color = "orange" if positive else "blue"
            s.rect(x, y, w, 210, stroke=color)
            s.frame(x+20, y+22, 118, 78, 3 if positive else 0, color)
            s.text(x+164, y+51, f"Frame at {sec} s", 26, color, 700)
            s.text(x+164, y+83, "Inside event" if positive else "Outside event", 19, "muted")
            s.text(x+20, y+142, "Abnormal now?", 22)
            pill(s, x+304, y+116, 156, "YES" if positive else "NO", color)
            s.text(x+20, y+186, "Which event?", 22)
            pill(s, x+304, y+160, 156, "falling" if positive else "normal", color)
        y = 1562
        s.rect(28, y, 484, 132, fill="#201f32", stroke="purple")
        s.text(48, y+35, "ONE TRAINING ITEM", 14, "purple", 700)
        s.text(48, y+74, "Frame + fixed question → GT answer", 23, weight=700)
        s.text(48, y+108, "XML supplies the label, not model input", 19, "muted")
        s.text(32, 1734, "Reported L3: one frame per decision", 21, "green", 700)
        s.text(32, 1767, "Data: falling + abandoned object", 19, "muted")
        s.text(32, 1800, "Example times and frames · prompts shortened", 17, "muted")
    else:
        s.label(52, 643, "3", "Add the two fixed questions", "green")
        for x, sec in [(32, 15), (460, 25), (888, 35)]:
            color = "orange" if sec==25 else "blue"
            s.rect(x, 668, 400, 228, stroke=color)
            s.frame(x+20, 690, 108, 70, 3 if sec==25 else 0, color)
            s.text(x+152, 717, f"Frame at {sec} s", 25, color, 700)
            s.text(x+152, 749, "Inside event" if sec==25 else "Outside event", 18, "muted")
            s.text(x+20, 806, "Abnormal now?", 21)
            pill(s, x+250, 782, 130, "YES" if sec==25 else "NO", color)
            s.text(x+20, 866, "Which event?", 21)
            pill(s, x+250, 842, 130, "falling" if sec==25 else "normal", color)
        s.rect(32, 924, 1256, 62, fill="#201f32", stroke="purple", r=10)
        s.text(56, 963, "Frame + fixed question → GT answer", 25, "purple", 700)
        s.text(688, 963, "XML supplies the label, not model input", 22, "muted")
        s.text(32, 1020, "Reported L3: single frame · Data: falling + abandoned object · Example times and frames; prompts shortened", 18, "muted")
    s.finish("cctv-training-labels"+("-mobile" if mobile else "")+".svg")


def layer_stack(s, x, y, w):
    s.text(x, y, "LAYA-VISION · 201M", 15, "green", 700)
    s.rect(x, y+22, w, 56, fill="#203040", stroke="blue", r=8)
    s.text(x+16, y+57, "Vision encoder", 23, "blue", 700)
    s.text(x+w-16, y+57, "FROZEN", 14, "blue", 700, "end")
    s.text(x, y+112, "Language layers", 20, "muted")
    cw = (w-16)/5
    for i in range(20):
        xx, yy = x+(i%5)*(cw+4), y+130+(i//5)*35
        color = "orange" if i>=16 else "blue"
        s.rect(xx, yy, cw, 27, fill="#413426" if i>=16 else "#203040", stroke=color, r=4)
        s.text(xx+cw/2, yy+19, i+1, 14, color, 700, "middle")
    s.rect(x, y+287, w, 56, fill="#413426", stroke="orange", r=8)
    s.text(x+16, y+323, "Decision head", 23, "orange", 700)
    s.text(x+w-16, y+323, "UPDATE", 14, "orange", 700, "end")
    s.text(x, y+377, "Blue: fixed weights", 19, "blue")
    s.text(x, y+408, "Orange: last 4 layers + head", 19, "orange")


def training_loop(mobile=False):
    s = SVG(540 if mobile else 1320, 2070 if mobile else 1080,
            "How the reported CCTV fine-tune updates Laya-Vision",
            "The experiment report describes single-frame RLCD fine-tuning of the decision head and last four language layers, with the vision encoder frozen. Image and question enter the model; XML-derived targets feed the training objective only. A conceptual update loop is shown without measured probabilities. The pinned upstream VLM objective combines cross-entropy and a policy-gradient term, but the CCTV run's loss coefficients and schedule have not been audited. Temperature fitting was attempted on held-out training videos; the reported calibration remained poor. Testing uses separate test videos.")
    s.header("05", "What changes during fine-tuning?", mobile)
    s.text(32, 112, "Reported L3 · single-frame training · XML-derived labels", 17 if mobile else 21, "muted")
    if mobile:
        s.rect(28, 144, 484, 156, stroke="purple")
        s.frame(48, 170, 118, 78, 3)
        s.text(194, 194, "Frame + question", 25, "purple", 700)
        s.text(194, 228, "“Abnormal now?”", 21)
        s.text(48, 278, "Label travels separately to the training objective", 17, "muted")
        s.line(270, 304, 270, 336, "purple", arrow=True)
        s.rect(28, 350, 484, 460, stroke="green")
        layer_stack(s, 48, 385, 444)
        s.line(270, 814, 270, 846, "green", arrow=True)
        s.rect(28, 860, 484, 150, stroke="green")
        s.text(48, 897, "MODEL OUTPUT", 14, "green", 700)
        s.text(48, 940, "Probability of each answer", 26, weight=700)
        for i, (label, w) in enumerate([("No", 108), ("Yes", 220)]):
            s.text(48+i*224, 978, label, 18, "muted")
            s.rect(90+i*224, 963, w*.65, 17, fill="green", stroke="none", r=3)
        s.line(270, 1014, 270, 1046, "green", arrow=True)
        s.rect(28, 1060, 484, 184, stroke="orange")
        s.text(48, 1097, "TRAINING OBJECTIVE", 14, "orange", 700)
        s.text(48, 1139, "Compare predictions with targets", 25, weight=700)
        pill(s, 48, 1170, 176, "GT: YES", "purple")
        s.line(244, 1187, 278, 1187, "purple", arrow=True)
        s.text(300, 1194, "Loss / reward", 22, "orange", 700)
        s.rect(28, 1268, 484, 102, fill="#413426", stroke="orange")
        s.text(48, 1308, "Update orange weights", 28, "orange", 700)
        s.text(48, 1345, "Repeat over balanced training samples", 21)
        # Feedback runs outside the cards and returns only to trainable layers.
        s.path("M28 1318 H12 V698 H28", "orange", arrow=True)
        objective_y = 1396
    else:
        s.rect(32, 154, 288, 460, stroke="purple")
        s.text(56, 191, "MODEL INPUT", 14, "purple", 700)
        s.frame(56, 217, 240, 148, 3)
        s.text(56, 407, "One CCTV frame", 25, weight=700)
        s.text(56, 449, "+ fixed question", 25, "purple", 700)
        s.text(56, 488, "“Abnormal now?”", 21)
        s.text(56, 582, "XML label stays outside", 19, "muted")
        s.line(325, 380, 368, 380, "purple", arrow=True)
        s.rect(380, 154, 416, 460, stroke="green")
        layer_stack(s, 404, 191, 368)
        s.rect(860, 154, 428, 192, stroke="green")
        s.text(884, 191, "MODEL OUTPUT", 14, "green", 700)
        s.text(884, 234, "Answer probabilities", 27, weight=700)
        for i,(label,width) in enumerate([("No",90),("Yes",200)]):
            yy=275+i*35
            s.text(884, yy, label, 20, "muted")
            s.rect(948, yy-16, width, 17, fill="green", stroke="none", r=3)
        s.path("M800 380 H822 V250 H850", "green", arrow=True)
        s.line(1074, 350, 1074, 376, "green", arrow=True)
        s.rect(860, 390, 428, 224, stroke="orange")
        s.text(884, 427, "TRAINING OBJECTIVE", 14, "orange", 700)
        s.text(884, 469, "Predictions ↔ targets", 27, weight=700)
        pill(s, 884, 499, 154, "GT: YES", "purple")
        s.line(1055, 516, 1086, 516, "purple", arrow=True)
        s.text(1105, 524, "Loss / reward", 20, "orange", 700)
        s.text(884, 581, "Target derived from XML event times", 18, "muted")
        s.path("M1074 618 V662 H588 V618", "orange", arrow=True)
        s.rect(666, 642, 363, 40, fill="bg", stroke="none", r=0)
        s.text(684, 668, "Update orange weights · repeat", 20, "orange", 700)
        objective_y = 710

    # The actual CCTV configuration is unavailable; never promote upstream
    # defaults into reported experimental settings.
    if mobile:
        s.rect(28, objective_y, 484, 236, fill="#201f32", stroke="purple", dash=True)
        s.text(48, objective_y+35, "REPORTED METHOD: RLCD", 16, "purple", 700)
        s.text(48, objective_y+76, "Pinned upstream objective", 23, weight=700)
        s.text(48, objective_y+116, "Cross-entropy", 24, "purple", 700)
        s.text(48, objective_y+150, "+ policy-gradient term", 24, "purple", 700)
        s.text(48, objective_y+189, "CCTV run coefficients and schedule:", 19, "muted")
        s.text(48, objective_y+220, "not yet verified from its training script", 19, "orange")
        s.text(32, 1674, "AFTER WEIGHT UPDATES", 15, "green", 700)
        s.rect(28, 1694, 484, 130, stroke="purple")
        s.text(48, 1733, "Held-out train videos", 26, "purple", 700)
        s.text(48, 1772, "Fit temperature → adjust probability scale", 20)
        s.text(48, 1806, "Reported calibration remained poor", 20, "orange")
        s.line(270, 1828, 270, 1854, "green", arrow=True)
        s.rect(28, 1868, 484, 120, stroke="green")
        s.text(48, 1907, "Separate test videos", 26, "green", 700)
        s.text(48, 1945, "Measure detection + calibration", 23)
        s.text(48, 1974, "Test annotations are for evaluation", 18, "muted")
        s.text(32, 2026, "Supervision: temporal labels → frame targets", 19, "muted")
        s.text(32, 2056, "Schematic probability bars · no measured values", 17, "muted")
    else:
        s.rect(32, objective_y, 1256, 132, fill="#201f32", stroke="purple", dash=True)
        s.text(56, objective_y+34, "REPORTED METHOD: RLCD", 15, "purple", 700)
        s.text(56, objective_y+80, "Upstream: cross-entropy + policy-gradient term", 26, "purple", 700)
        s.text(56, objective_y+113, "Pinned upstream recipe; the CCTV run's loss coefficients and schedule have not been verified.", 19, "muted")
        s.text(32, 884, "AFTER WEIGHT UPDATES", 14, "green", 700)
        s.rect(32, 904, 584, 112, stroke="purple")
        s.text(56, 941, "Held-out train videos → temperature fit", 23, "purple", 700)
        s.text(56, 981, "Adjust score scale · reported calibration remained poor", 19, "orange")
        s.line(624, 959, 680, 959, "green", arrow=True)
        s.rect(696, 904, 592, 112, stroke="green")
        s.text(720, 941, "Separate test videos → evaluation", 24, "green", 700)
        s.text(720, 981, "Detection + calibration · test labels used for metrics", 19, "muted")
        s.text(32, 1054, "Supervision: temporal labels → frame targets · Balanced training samples · Probability bars are schematic", 18, "muted")
    s.finish("cctv-finetuning-loop"+("-mobile" if mobile else "")+".svg")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mobile in (False, True):
        label_data(mobile)
        training_loop(mobile)
    print("Built 4 fine-tuning SVGs (desktop and mobile variants).")
