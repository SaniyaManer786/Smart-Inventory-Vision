from ultralytics import YOLO
import os

print("🔥 TESTING YOUR MODELS...")
print("📁 Current folder files:")
for f in os.listdir('.'):
    if f.endswith('.pt'):
        print(f"✅ FOUND: {f} ({os.path.getsize(f)/1024/1024:.1f} MB)")

# 🔥 TEST ALL 3 MODELS!
models = {}

# 1. YOUR BEST MODEL
if os.path.exists('best.pt'):
    print("\n" + "="*50)
    print("🟢 BEST.PT (YOUR CUSTOM - BEST PERFORMANCE)")
    model = YOLO('best.pt')
    models['best'] = model
    print("CLASSES:", model.names)
    print("TOTAL CLASSES:", len(model.names))

# 2. YOUR LAST EPOCH  
if os.path.exists('last.pt'):
    print("\n" + "="*50)
    print("🟡 LAST.PT (YOUR CUSTOM - FINAL EPOCH)")
    model = YOLO('last.pt')
    models['last'] = model
    print("CLASSES:", model.names)
    print("TOTAL CLASSES:", len(model.names))

# 3. STANDARD YOLOv8N
if os.path.exists('yolov8n.pt'):
    print("\n" + "="*50)
    print("🔵 YOLOv8N.PT (COCO 80 classes)")
    model = YOLO('yolov8n.pt')
    models['yolov8n'] = model
    print("CLASSES (first 10):", {k: v for k, v in list(model.names.items())[:10]})
    print("BOTTLE CLASS:", 44 in model.names and model.names[44])
    print("PHONE CLASS:", 67 in model.names and model.names[67])

print("\n" + "="*50)
print("🎯 RECOMMENDATION:")
if 'best' in models:
    print("✅ USE 'best.pt' - YOUR BEST CUSTOM MODEL!")
elif 'last' in models:
    print("✅ USE 'last.pt' - YOUR CUSTOM MODEL")
else:
    print("✅ USE 'yolov8n.pt' - Standard model")

print("\n📋 COPY YOUR CLASSES OUTPUT ABOVE → Put in utils.py!")
