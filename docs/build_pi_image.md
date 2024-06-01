Building a custom Raspberry Pi image from the OS of an SD card on a Mac involves several steps. Here's a detailed step-by-step guide:

### Step 1: Insert the SD Card
1. Insert the SD card into your Mac using an SD card reader.

### Step 2: Identify the SD Card
1. Open Terminal (you can find it in Applications > Utilities).
2. Type the following command to list all disks and identify your SD card:

   ```bash
   diskutil list
   ```

   Look for your SD card in the list (it will typically be something like `/dev/disk2`).

### Step 3: Unmount the SD Card
1. Unmount the SD card so that it can be copied:

   ```bash
   diskutil unmountDisk /dev/disk2
   ```

   Replace `/dev/disk2` with your SD card identifier.

### Step 4: Create an Image of the SD Card
1. Use the `dd` command to create an image of the SD card. This can take some time depending on the size of the card.

   ```bash
   sudo dd if=/dev/disk2 of=~/Desktop/raspberrypi.img bs=1m status=progress
   ```

   Again, replace `/dev/disk2` with your SD card identifier. This command will create a file called `raspberrypi.img` on your desktop.

### Step 5: Verify the Image
1. You can verify the image by mounting it and checking the files:

   ```bash
   hdiutil attach ~/Desktop/raspberrypi.img
   ```

   This will mount the image and you can browse it in Finder to ensure it contains your files.

### Step 6: Unmount the Image
1. After verifying, unmount the image:

   ```bash
   hdiutil detach /dev/diskX
   ```

   Replace `/dev/diskX` with the actual identifier of the mounted image.

### Step 7: Compress the Image Using Gzip
1. Compress the `.img` file using gzip to save space:

   ```bash
   gzip ~/Desktop/raspberrypi.img
   ```

   This will create a file called `raspberrypi.img.gz` on your desktop.

### Step 8: Clean Up
1. If everything is successful and you have verified your image, you can safely eject your SD card:

   ```bash
   diskutil eject /dev/disk2
   ```

   Replace `/dev/disk2` with your SD card identifier.

Now you have a compressed `.img.gz` file of your Raspberry Pi OS, which you can use to restore the system or distribute as needed.