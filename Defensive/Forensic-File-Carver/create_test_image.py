import os

def create_test_image(filename="test_disk.dd", size_mb=5):
    """
    Creates a dummy disk image file with two embedded JPEG files for testing.
    """
    # Size of the file in bytes
    file_size = size_mb * 1024 * 1024
    
    # --- A Simple, Valid JPEG File Structure (in bytes) ---
    # SOI (Start of Image)
    jpeg_header = b'\xff\xd8\xff\xe0'
    # Some placeholder application data
    jpeg_app_data = b'\x00\x10JFIF\x00\x01\x01\x01\x00\x48\x00\x48\x00\x00'
    # Some placeholder image data
    jpeg_image_data = b'This is some sample image data... ' * 5
    # EOI (End of Image)
    jpeg_footer = b'\xff\xd9'

    jpeg_file_1 = jpeg_header + jpeg_app_data + jpeg_image_data + jpeg_footer
    jpeg_file_2 = jpeg_header + jpeg_app_data + (b'This is the second image! ' * 5) + jpeg_footer

    print(f"Creating a {size_mb}MB disk image named '{filename}'...")

    try:
        with open(filename, 'wb') as f:
            # --- Write the file content ---

            # 1. Start with some "junk" data to simulate other files/noise
            f.write(os.urandom(1024 * 500)) # 500 KB of random data

            # 2. Write our first JPEG file
            print(f"Embedding first JPEG at offset {f.tell()} bytes.")
            f.write(jpeg_file_1)

            # 3. Write more junk data between the JPEGs
            f.write(os.urandom(1024 * 1024 * 2)) # 2 MB of random data

            # 4. Write our second JPEG file
            print(f"Embedding second JPEG at offset {f.tell()} bytes.")
            f.write(jpeg_file_2)

            # 5. Fill the rest of the file with junk data to reach the desired size
            remaining_size = file_size - f.tell()
            if remaining_size > 0:
                f.write(os.urandom(remaining_size))
        
        print(f"\nSuccessfully created '{filename}' ({os.path.getsize(filename) / (1024*1024):.2f} MB).")
        print("You can now use this file as the input for your recovery script.")

    except IOError as e:
        print(f"Error creating file: {e}")


if __name__ == "__main__":
    create_test_image()