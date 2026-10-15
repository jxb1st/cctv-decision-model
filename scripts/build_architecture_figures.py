"""Build the editable, self-contained SVG figures used by index.html.

Run: python3 scripts/build_architecture_figures.py
Architecture: thaitea/laya-vision @ f2fe3c12cb6d04c59d8a190250bf3fb40fc828dc.
All video thumbnails and output values are schematic, not experiment footage.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
C = dict(bg="#10171f", panel="#19232e", line="#344354", ink="#edf3fa",
         muted="#a2b2c3", blue="#70baff", green="#83dfb0", purple="#c0adff", orange="#ffbf79")


class SVG:
    def __init__(self, width, height, title, desc):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                      '<defs>' + ''.join(f'<marker id="arrow-{name}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M1 1 L7 4 L1 7" fill="none" stroke="{color}" stroke-width="1.5"/></marker>' for name, color in C.items()) + '</defs>',
                      f'<rect width="{width}" height="{height}" rx="20" fill="{C["bg"]}"/>']

    def rect(self, x, y, w, h, fill="panel", stroke="line", r=14, dash=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{C.get(fill, fill)}" stroke="{C.get(stroke, stroke)}" stroke-width="1.5"' + (' stroke-dasharray="6 5"' if dash else '') + '/>')

    def text(self, x, y, text, size=20, color="ink", weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{C.get(color,color)}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(text))}</text>')

    def line(self, x1, y1, x2, y2, color="line", width=2, dash=False, arrow=False):
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{C[color]}" stroke-width="{width}"' + (' stroke-dasharray="6 5"' if dash else '') + (f' marker-end="url(#arrow-{color})"' if arrow else '') + '/>')

    def path(self, d, color="muted", dash=False, arrow=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="{C[color]}" stroke-width="2"' + (' stroke-dasharray="6 5"' if dash else '') + (f' marker-end="url(#arrow-{color})"' if arrow else '') + '/>')

    def circle(self, x, y, r, fill):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C.get(fill,fill)}"/>')

    def label(self, x, y, num, title, color="blue"):
        self.circle(x+13, y-7, 13, color)
        self.text(x+13, y-2, num, 14, "bg", 700, "middle")
        self.text(x+36, y, title, 20, color, 700)

    def header(self, number, title, mobile=False):
        self.text(32, 36, f"{number} / CCTV DECISION MODEL", 13, "blue", 700)
        self.text(32, 78, title, 28 if mobile else 34, weight=700)

    def frame(self, x, y, w, h, pose=0, color="blue"):
        self.rect(x,y,w,h,fill="#203040",stroke=color,r=6)
        self.path(f'M{x+8} {y+h-14} L{x+w-8} {y+h-14}',"line")
        self.path(f'M{x+8} {y+h-15} L{x+8} {y+14} L{x+28} {y+14} L{x+28} {y+h-15}',"line")
        px,py=x+w*.62,y+h*.42
        if pose<3:
            self.circle(px,py,4,color)
            self.path(f'M{px} {py+6} l{pose*3} 14 l-8 12 M{px+pose*3} {py+20} l9 12 M{px} {py+9} l-9 6 M{px} {py+9} l9 6',color)
        else:
            self.circle(px+12,py+18,4,color)
            self.path(f'M{px+6} {py+18} h-15 l-11 3 M{px-9} {py+18} l-8 -5',color)

    def finish(self, name):
        OUT.joinpath(name).write_text('\n'.join(self.parts)+"\n</svg>\n")


def model_family(mobile=False):
    s = SVG(540 if mobile else 1320, 1740 if mobile else 900,
            "Jev, Laya and Laya-Vision: what each model does",
            "Jev is TypeSafe's hosted decision service. Laya is an independent open-source text decision model with a compatible API, not an official release of Jev's weights. Laya-Vision is an independent code fork of Laya that adds image input using a small vision-language backbone. This CCTV experiment uses Laya-Vision directly, without a Jev API call. Shared outputs include choices, scores and yes/no probabilities.")
    s.header("00", "Meet the decision models", mobile)

    # A shared task, followed by a relationship map. Dashed links mean API
    # compatibility; only the solid arrow denotes an actual code extension.
    if mobile:
        s.rect(28,110,484,108,fill="#1c2632",r=12)
        s.text(48,143,"WHAT A DECISION MODEL DOES",13,"blue",700)
        s.text(48,179,"Content + question",20,weight=700)
        s.line(235,172,267,172,"blue",arrow=True)
        s.text(286,166,"Choice / score",19,"green",700)
        s.text(286,193,"Yes/no probability",17,"muted")
        panels = [(28,250,484,280),(28,650,484,280),(28,1050,484,280)]
    else:
        s.rect(32,112,1256,104,fill="#1c2632",r=12)
        s.rect(56,135,42,55,fill="#203040",stroke="blue",r=6)
        for i,w in enumerate([24,24,15]): s.line(65,150+i*12,65+w,150+i*12,"blue",width=2)
        s.text(118,162,"Content + question",24,weight=700)
        s.text(118,190,"You define the judgment",17,"muted")
        s.line(392,164,458,164,"blue",arrow=True)
        s.text(498,162,"Decision model",24,"green",700)
        s.text(498,190,"Direct numerical answers",17,"muted")
        s.line(760,164,826,164,"green",arrow=True)
        for x,label,value in [(868,"CHOOSE","A / B / C"),(1008,"RATE","0 … 3"),(1148,"YES / NO","0 … 1")]:
            s.text(x,147,label,12,"muted",700)
            s.text(x,184,value,24,"green",700)
        panels = [(32,266,340,324),(490,266,340,324),(948,266,340,324)]

    for i,(x,y,w,h) in enumerate(panels):
        color = ["blue","purple","green"][i]
        s.rect(x,y,w,h,fill="#1d2a30" if i==2 else "panel",stroke=color)
        s.text(x+24,y+48,["Jev","Laya","Laya-Vision"][i],34,color,700)
        s.text(x+24,y+78,["TypeSafe AI","Convai Innovations","Independent Laya fork"][i],17,"muted")
        ix,iy = x+24,y+106
        if i==0:
            # Cloud with three service endpoints.
            s.path(f'M{ix+18} {iy+52} C{ix-4} {iy+52} {ix-4} {iy+23} {ix+18} {iy+22} C{ix+23} {iy-5} {ix+60} {iy-4} {ix+66} {iy+22} C{ix+91} {iy+19} {ix+94} {iy+52} {ix+69} {iy+52} Z',color)
            for dx in [20,43,66]:
                s.line(ix+dx,iy+53,ix+dx,iy+71,color)
                s.circle(ix+dx,iy+76,4,color)
        elif i==1:
            # A locally runnable model, depicted as a server and code brackets.
            for dy in [0,27,54]:
                s.rect(ix,iy+dy,86,21,fill="#252239",stroke=color,r=5)
                s.circle(ix+12,iy+dy+10,3,color)
                s.line(ix+28,iy+dy+10,ix+73,iy+dy+10,color,width=1)
        else:
            s.frame(ix+12,iy,84,62,3,color)
            s.frame(ix,iy+16,84,62,0,color)
        tx,ty = (x+156,y+144) if mobile else (x+24,y+204)
        s.text(tx,ty,["Hosted service","Open-source text model","Visual decision model"][i],23 if mobile else 24,weight=700)
        s.text(tx,ty+31,["Call a remote API","Run + fine-tune locally","Images + text questions"][i],18,"muted")
        if i==0:
            s.rect(tx,ty+59,164,32,fill="#203040",stroke="blue",r=6)
            s.text(tx+82,ty+81,"COMMERCIAL",14,"blue",700,"middle")
        elif i==1:
            s.text(tx,ty+84,"421M / 322M",24,"purple",700)
            s.text(tx+172,ty+84,"parameters",16,"muted")
        else:
            s.text(tx,ty+84,"201M",28,"green",700)
            s.rect(tx+137,ty+59,146,32,fill="#254039",stroke="green",r=6)
            s.text(tx+210,ty+81,"USED HERE",14,"green",700,"middle")

    if mobile:
        s.line(270,534,270,644,"blue",dash=True)
        s.rect(94,560,352,56,fill="bg",stroke="none",r=0)
        s.text(270,582,"Compatible API",21,"blue",700,"middle")
        s.text(270,608,"Independent models",18,"muted",anchor="middle")
        s.line(270,934,270,1040,"purple",arrow=True)
        s.rect(110,954,320,58,fill="bg",stroke="none",r=0)
        s.text(270,977,"Code fork + image input",21,"purple",700,"middle")
        s.text(270,1004,"Uses a small VLM backbone",18,"muted",anchor="middle")
        s.text(32,1374,"Laya is an independent alternative to Jev.",19,"muted")
        s.rect(28,1410,484,292,fill="#1d2a30",stroke="green")
        s.text(48,1447,"OUR CCTV EXPERIMENT",14,"green",700)
        for i in range(3): s.frame(48+i*24,1484-i*8,96,60,i,"blue")
        s.text(226,1500,"Video frames + question",20)
        s.line(380,1512,380,1539,"green",arrow=True)
        s.rect(48,1550,444,64,fill="#254039",stroke="green",r=10)
        s.text(270,1591,"Laya-Vision · 201M",27,"green",700,"middle")
        s.text(48,1651,"→ Event + anomaly score",22,weight=700)
        s.text(48,1683,"Runs directly · no Jev API call",18,"muted")
    else:
        s.line(378,410,484,410,"blue",dash=True)
        s.text(431,366,"Compatible",16,"blue",700,"middle")
        s.text(431,389,"API",16,"blue",700,"middle")
        s.text(431,446,"Independent",15,"muted",anchor="middle")
        s.text(431,468,"models",15,"muted",anchor="middle")
        s.line(836,410,940,410,"purple",arrow=True)
        s.text(889,366,"Code",16,"purple",700,"middle")
        s.text(889,389,"fork",16,"purple",700,"middle")
        s.text(889,446,"Adds",16,"muted",anchor="middle")
        s.text(889,468,"vision",16,"muted",anchor="middle")
        s.text(32,629,"Laya is an independent alternative to Jev.",19,"muted")
        s.text(720,629,"Laya-Vision replaces the text encoder with a small VLM.",18,"muted")
        s.rect(32,662,1256,206,fill="#1d2a30",stroke="green")
        s.text(56,699,"OUR CCTV EXPERIMENT",14,"green",700)
        for i in range(3): s.frame(56+i*24,738-i*8,96,60,i,"blue")
        s.text(224,754,"Video frames",22,weight=700)
        s.text(224,784,"+ question",19,"muted")
        s.line(402,758,458,758,"green",arrow=True)
        s.rect(476,722,350,74,fill="#254039",stroke="green",r=10)
        s.text(651,769,"Laya-Vision · 201M",28,"green",700,"middle")
        s.line(844,758,900,758,"green",arrow=True)
        s.text(928,754,"Event + anomaly score",23,weight=700)
        s.text(928,784,"Numerical outputs",19,"muted")
        s.text(56,843,"Runs directly · no Jev API call",19,"green")
    s.finish("decision-model-family"+("-mobile" if mobile else "")+".svg")


def pipeline(mobile=False):
    s=SVG(540 if mobile else 1320, 1500 if mobile else 710,
          "CCTV inference inputs, decisions and training path",
          "Video is sampled at one frame per second. One frame or the last four frames, plus fixed questions, enter Laya-Vision. It returns an anomaly score and a six-way event distribution. Thresholds produce alarms. XML labels are used only in offline training and evaluation. All thumbnails and numerical outputs are illustrative.")
    s.header("01", "From video to decisions", mobile)
    if mobile:
        s.rect(28,110,484,190); s.label(48,145,"1","Sample the video")
        for i in range(4): s.frame(48+i*111,171,99,62,i)
        s.text(48,270,"1 fps · 640 × 360 · latest 1 or 4 frames",20,"muted")
        s.line(270,302,270,330,"blue",arrow=True)
        s.rect(28,342,484,136,stroke="purple"); s.label(48,378,"2","Add fixed questions","purple")
        s.text(48,416,"Abnormal now?     Which event?",22)
        s.text(48,450,"Context: judge the latest frame",19,"muted")
        s.line(270,480,270,510,"purple",arrow=True)
        s.rect(28,522,484,154,stroke="green"); s.label(48,558,"3","Laya-Vision","green")
        s.text(48,612,"201M",44,"green",700); s.text(224,600,"Images + text → scores",22)
        s.text(224,636,"No generated description",18,"muted")
        s.line(270,678,270,708,"green",arrow=True)
        ox,oy,ow=28,720,484
    else:
        xs=[32,260,540,804,1104]; ws=[196,248,232,268,184]
        for x,w in zip(xs,ws): s.rect(x,142,w,294)
        for i,(a,b) in enumerate(zip(xs,xs[1:])): s.line(a+ws[i]+4,280,b-8,280,"blue",arrow=True)
        s.label(48,180,"1","Video")
        s.frame(56,216,148,91)
        s.text(56,349,"CCTV clip",22,weight=700); s.text(56,383,"1080p · 30 fps",18,"muted")
        s.label(276,180,"2","Sample frames")
        for i in range(4): s.frame(280+i*16,232-i*9,152,84,i)
        s.text(280,350,"1 frame / last 4",22,weight=700)
        s.text(280,383,"1 fps · 640 × 360",18,"muted")
        s.label(556,180,"3","Laya-Vision","green")
        s.rect(597,214,118,88,fill="#213a34",stroke="green",r=12)
        for i in range(4):
            s.line(588,230+i*18,597,230+i*18,"green"); s.line(715,230+i*18,724,230+i*18,"green")
        s.text(656,269,"201M",33,"green",700,"middle")
        s.text(562,350,"Direct decision",22,weight=700); s.text(562,383,"No text generation",18,"muted")
        ox,oy,ow=804,142,268
    # The output card is deliberately illustrative; no experiment prediction is fabricated.
    if mobile: s.rect(ox,oy,ow,300)
    s.label(ox+16,oy+38,"4","Typed outputs","green")
    s.text(ox+20,oy+75,"anomaly",18,"muted"); s.text(ox+ow-20,oy+75,"0.82",22,"green",700,"end")
    s.rect(ox+20,oy+91,ow-40,7,fill="line",stroke="line",r=3)
    s.rect(ox+20,oy+91,(ow-40)*.82,7,fill="green",stroke="green",r=3)
    vals=[("normal",.15),("fight",.02),("falling",.75),("abandoned",.03),("loitering",.03),("intrusion",.02)]
    for i,(label,value) in enumerate(vals):
        y=oy+129+i*21
        s.text(ox+20,y,label,15,"ink" if label=="falling" else "muted")
        barx=ox+118; barw=ow-170
        s.rect(barx,y-10,max(3,barw*value),8,fill="green" if label=="falling" else "blue",stroke="none",r=2)
        s.text(ox+ow-20,y,f"{value:.2f}",14,"muted",anchor="end")
    s.text(ox+20,oy+278,"Illustrative values",15,"muted")
    if mobile:
        s.line(270,1022,270,1052,"green",arrow=True)
        s.rect(28,1064,484,98,stroke="orange"); s.label(48,1100,"5","Alarm policy","orange")
        s.text(48,1135,"Score ≥ threshold → alert at latest frame",20)
        tx,ty,tw=28,1224,484
        s.text(32,1203,"OFFLINE ONLY",14,"purple",700)
        s.rect(tx,ty,tw,214,fill="#201f32",stroke="purple",dash=True)
        s.text(48,1260,"Train frames + XML event spans",22,"purple",700)
        s.text(48,1300,"RLCD: head + last 4 LM layers",21)
        s.text(48,1336,"Held-out videos → temperature fit",20)
        s.text(48,1372,"Updated weights + temperatures → model",19,"muted")
        s.text(48,1410,"Test XML → metrics only",20,"muted")
        s.text(32,1473,"Schematics only · no private CCTV footage",17,"muted")
    else:
        s.label(1120,180,"5","Policy","orange")
        s.text(1196,255,"≥ τ",42,"orange",700,"middle")
        s.text(1196,305,"Threshold",20,anchor="middle")
        s.text(1196,350,"Alert / no alert",18,anchor="middle")
        s.text(1196,383,"Latest frame",17,"muted",anchor="middle")
        s.rect(260,470,512,80,fill="#252239",stroke="purple")
        s.text(280,500,"FIXED QUESTIONS + CONTEXT",14,"purple",700)
        s.text(280,529,"Abnormal now?  ·  Which event?  ·  Judge latest frame",18)
        s.line(656,469,656,442,"purple",arrow=True)
        s.text(32,554,"OFFLINE TRAINING",14,"purple",700)
        s.rect(32,570,1256,94,fill="#201f32",stroke="purple",dash=True)
        for x,title,sub in [(52,"Train frames + XML","Temporal event labels"),(360,"RLCD fine-tuning","Head + last 4 LM layers"),(690,"Temperature fit","Held-out train videos"),(1008,"Model artifacts","Weights + temperatures")]:
            s.text(x,604,title,21,"purple",700); s.text(x,638,sub,18,"muted")
        for x in [307,636,958]: s.line(x,615,x+34,615,"purple",dash=True,arrow=True)
        s.text(32,694,"Training labels are offline only. Test XML is used for metrics. Output values and frame thumbnails are illustrative.",17,"muted")
    s.finish("cctv-pipeline"+("-mobile" if mobile else "")+".svg")


def architecture(mobile=False):
    s=SVG(540 if mobile else 1320,1600 if mobile else 730,"Inside the 201M Laya-Vision model",
          "The selected checkpoint uses a SigLIP vision tower, a pixel-shuffle connector, and a SmolLM2 language backbone reduced to 20 layers. Image tokens and text enter the backbone, then a two-layer bidirectional decision head scores option markers. Temperature scaling and softmax return binary anomaly and six-way event outputs. The CCTV fine-tune updates the final four language layers and decision head.")
    s.header("02","Inside Laya-Vision",mobile)
    if mobile:
        s.rect(28,110,484,222,stroke="blue")
        s.text(48,146,"IMAGE PATH",14,"blue",700)
        s.frame(48,165,112,72)
        s.line(174,204,204,204,"blue",arrow=True)
        s.text(222,186,"SigLIP-B/16",24,weight=700)
        s.text(222,219,"12 layers · frozen",19,"muted")
        s.text(48,274,"512 × 512 → 1,024 visual patches",22)
        s.text(48,307,"Pixel shuffle + projection → 64 tokens/image",19,"blue")
        s.line(270,334,270,364,"blue",arrow=True)
        s.rect(28,376,484,160,stroke="purple")
        s.text(48,413,"ASSEMBLE THE INPUT",14,"purple",700)
        for i,(label,col) in enumerate([("Image tokens","blue"),("Context","purple"),("Question","purple"),("Options","purple")]):
            x=48+(i%2)*224; y=430+(i//2)*44
            s.rect(x,y,204,32,fill="#252239" if col=="purple" else "#203040",stroke=col,r=6); s.text(x+12,y+22,label,17,col)
        s.line(270,538,270,568,"purple",arrow=True)
        bx,by,bw,bh=28,580,484,352
    else:
        s.rect(32,138,324,280,stroke="blue")
        s.text(52,175,"IMAGE PATH",14,"blue",700)
        s.frame(52,196,92,62); s.line(156,228,183,228,"blue",arrow=True)
        s.text(200,218,"SigLIP-B/16",22,weight=700); s.text(200,249,"12 layers · frozen",16,"muted")
        s.text(52,296,"512 × 512 → 1,024 patches",20)
        s.rect(52,318,284,76,fill="#203040",stroke="blue",r=8)
        s.text(70,348,"Pixel shuffle + projection",20,"blue",700)
        s.text(70,378,"64 visual tokens per image",19)
        s.rect(32,444,324,176,stroke="purple")
        s.text(52,480,"TEXT PATH",14,"purple",700)
        for i,t in enumerate(["Context + temporal note","Question + candidate options"]): s.text(52,518+i*36,t,19)
        s.text(52,593,"Text tokens + option markers",17,"muted")
        s.path('M356 360 H382 V278 H404',"blue",arrow=True)
        s.path('M356 528 H382 V330 H404',"purple",arrow=True)
        bx,by,bw,bh=416,138,384,482
    s.rect(bx,by,bw,bh,fill="#1d2a30",stroke="green")
    s.text(bx+20,by+37,"LANGUAGE BACKBONE",14,"green",700)
    s.text(bx+20,by+79,"SmolLM2",30,weight=700)
    s.text(bx+20,by+111,"20 retained Transformer layers",20,"muted")
    # Exactly twenty retained layers; the final four are trainable for CCTV.
    gx,gy=bx+20,by+139
    cellw=(bw-58)/5
    for i in range(20):
        x=gx+(i%5)*(cellw+4.5); y=gy+(i//5)*39
        col="orange" if i>=16 else "green"
        s.rect(x,y,cellw,30,fill="#413426" if i>=16 else "#254039",stroke=col,r=5)
        s.text(x+cellw/2,y+21,str(i+1),15,col,700,"middle")
    if mobile:
        s.text(bx+20,by+329,"Orange: last 4 layers updated for CCTV",19,"orange")
        s.line(270,934,270,964,"green",arrow=True)
        hx,hy,hw=28,976,484
    else:
        s.text(bx+20,by+330,"d = 576 · 9 attention heads",20,"muted")
        s.text(bx+20,by+373,"Options attend to each other",20,"purple")
        s.text(bx+20,by+410,"Last 4 layers: CCTV fine-tuned",19,"orange")
        s.text(bx+20,by+449,"Hidden states → decision head",19,"green")
        s.line(804,340,844,340,"green",arrow=True)
        hx,hy,hw=856,138,432
    s.rect(hx,hy,hw,280,stroke="orange")
    s.text(hx+20,hy+37,"DECISION READOUT",14,"orange",700)
    s.text(hx+20,hy+78,"2 bidirectional Transformer layers",21,weight=700)
    for i,label in enumerate(["normal","falling","…"]):
        x=hx+20+i*(hw-40)/3
        s.rect(x,hy+105,(hw-58)/3,46,fill="#302a42",stroke="purple",r=7)
        s.text(x+(hw-58)/6,hy+134,label,18,"purple",anchor="middle")
    s.text(hx+20,hy+183,"Read each option's marker",21)
    s.line(hx+hw/2,hy+195,hx+hw/2,hy+214,"orange",arrow=True)
    s.text(hx+hw/2,hy+250,"Shared scorer → one logit / option",20,"orange",700,"middle")
    if mobile:
        s.line(270,1258,270,1288,"orange",arrow=True)
        ox,oy,ow=28,1300,484
    else:
        s.line(hx+hw/2,421,hx+hw/2,440,"orange",arrow=True)
        ox,oy,ow=856,452,432
    s.rect(ox,oy,ow,168,stroke="green")
    s.text(ox+20,oy+35,"Temperature + softmax",23,"green",700)
    s.text(ox+20,oy+76,"noul       yes / no → anomaly score",20)
    s.text(ox+20,oy+111,"choice    6 events → distribution",20)
    s.text(ox+20,oy+145,"Scores need domain calibration",18,"muted")
    if mobile:
        s.text(32,1510,"201M parameters · existing Transformer backbone",18,"muted")
        s.text(32,1543,"CCTV update: decision head + last 4 LM layers",18,"orange")
        s.text(32,1575,"Auxiliary act head omitted from this task view",17,"muted")
    else:
        s.rect(32,648,1256,50,fill="#1c2632",stroke="line",r=10)
        s.text(52,680,"201M total",21,"green",700)
        s.text(224,680,"Existing Transformer backbone",19)
        s.text(584,680,"CCTV: head + last 4 LM layers",19,"orange")
        s.text(943,680,"Auxiliary act head omitted",17,"muted")
    s.finish("laya-vision-architecture"+("-mobile" if mobile else "")+".svg")


def compact(mobile=False):
    s=SVG(540 if mobile else 1320,1460 if mobile else 675,"Why Laya-Vision is small and how its decision output differs",
          "The 201M checkpoint starts with a compact SmolVLM backbone and retains 20 of its 30 language layers. It produces option scores directly rather than generating explanatory text. Compact networks and layer removal reduce parameter count; direct scoring avoids autoregressive answer generation. RLCD is a training objective, not a new language-model architecture. Qwen in this experiment also uses direct first-token scoring.")
    s.header("03","Why only 201M parameters?",mobile)
    panels=[(28,118,484,330),(28,472,484,352),(28,848,484,360)] if mobile else [(32,138,400,352),(460,138,400,352),(888,138,400,352)]
    x,y,w,h=panels[0]; s.rect(x,y,w,h,stroke="blue")
    s.label(x+20,y+36,"1","Start compact")
    s.text(x+20,y+89,"SmolVLM family",28,weight=700)
    s.text(x+20,y+126,"Small vision + language backbone",19,"muted")
    s.text(x+20,y+176,"Qwen reference",18); s.text(x+w-20,y+176,"27B",22,"muted",700,"end")
    s.rect(x+20,y+192,w-40,20,fill="line",stroke="line",r=3)
    s.text(x+20,y+251,"Laya-Vision",18); s.text(x+w-20,y+251,"0.201B",22,"blue",700,"end")
    s.rect(x+20,y+267,(w-40)*.201/27,20,fill="blue",stroke="blue",r=1)
    s.text(x+20,y+317,"Parameter counts · linear scale",17,"muted")
    x,y,w,h=panels[1]; s.rect(x,y,w,h,stroke="green")
    s.label(x+20,y+36,"2","Retain fewer layers","green")
    s.text(x+20,y+91,"30 → 20",42,"green",700)
    s.text(x+20,y+126,"Language-model layers",20,"muted")
    cell=(w-76)/10
    for i in range(30):
        xx=x+20+(i%10)*(cell+4); yy=y+155+(i//10)*37
        kept=i<20
        s.rect(xx,yy,cell,26,fill="#254039" if kept else "bg",stroke="green" if kept else "line",r=4,dash=not kept)
        if not kept: s.line(xx+6,yy+20,xx+cell-6,yy+6,"muted",width=1)
    s.text(x+20,y+290,"20 retained",19,"green",700)
    s.text(x+w-20,y+290,"10 removed",19,"muted",anchor="end")
    s.text(x+20,y+323,"Then continued training",19,"muted")
    x,y,w,h=panels[2]; s.rect(x,y,w,h,stroke="purple")
    s.label(x+20,y+36,"3","Read scores directly","purple")
    s.text(x+20,y+87,"Decision readout",27,weight=700)
    for i,(t,bh) in enumerate([("A",35),("B",76),("C",24)]):
        bx=x+62+i*72
        s.rect(bx,y+210-bh,40,bh,fill="purple",stroke="purple",r=4)
        s.text(bx+20,y+237,t,17,"muted",anchor="middle")
    s.line(x+20,y+213,x+w-20,y+213,"line",width=1)
    s.text(x+20,y+279,"One score per candidate option",19,"purple")
    s.text(x+20,y+313,"No generated answer sequence",19,"muted")
    if mobile:
        s.rect(28,1232,484,104,fill="#201f32",stroke="purple")
        s.text(48,1267,"RLCD = training objective",23,"purple",700)
        s.text(48,1305,"Parameter count and inference cost differ",19,"muted")
        s.text(32,1370,"Text Laya: ModernBERT + head · 421M",20,"muted")
        s.text(32,1405,"Qwen here also uses direct token scoring.",18,"muted")
        s.text(32,1436,"The parameter ratio is not a speedup claim.",18,"muted")
    else:
        s.rect(32,518,1256,58,fill="#201f32",stroke="purple",r=10)
        s.text(52,555,"RLCD = training objective",23,"purple",700)
        s.text(452,555,"Compact network → fewer parameters",20,"green")
        s.text(904,555,"Direct scoring → no answer decoding",18,"purple")
        s.text(32,615,"Related text model: Laya = ModernBERT + decision head · 421M parameters",20,"muted")
        s.text(32,651,"Qwen also uses direct token scoring in this experiment. Parameter ratio is not a measured speedup.",18,"muted")
    s.finish("why-laya-is-compact"+("-mobile" if mobile else "")+".svg")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mobile in (False,True):
        model_family(mobile)
        pipeline(mobile)
        architecture(mobile)
        compact(mobile)
    print("Built 8 SVGs (desktop and mobile variants).")
