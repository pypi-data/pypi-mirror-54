# **SPRITE-DETECTION PROJECT**
Sprite-detection is a tool using python library to detect sprite sheet in a image

This tool will help you spend less time when you want to detect sprite to making a game or animetion, ...

## **How to using this tool**
First you must **Download** our tool and import to your device

**Before start** using you should download all depencencies of this tool

Second pass an image path or Image object to **SpriteSheet** Object of our. That's it easy right^^.

### EXAMPLE: 
```
from sprite_detection_tool.spriteutil import SpriteSheet

a = SpriteSheet(path/Image object)
```

We have 2 method of SpriteSheet object in this tool you can using:

- find_sprites() method will return a list [sprites, label_map]

### EXAMPLE: 
```
from sprite_detection_tool.spriteutil import SpriteSheet

a = SpriteSheet(path/Image object)
sprites, label_map = a.find_sprites()
```

- create_sprite_labels_image() method **return an Image object**

### EXAMPLE: 
```
from sprite_detection_tool.spriteutil import SpriteSheet

a = SpriteSheet(path/Image object)
sprites, label_map = a.find_sprites()
create_sprite_labels_image(sprites, label_map).show()
```

## **How you can help**

- Use our community test server and write up issues
- If you are a developer, install the software for development