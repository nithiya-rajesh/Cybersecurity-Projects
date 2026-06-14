import os
import csv      # NEW: Import the csv library
import hashlib  # NEW: Import the hashlib library

# --- Constants ---
JPEG_SOI = b'\xff\xd8\xff\xe0'
JPEG_EOI = b'\xff\xd9'

def carve_files(disk_image_path, output_dir="recovered"):
    print(f"--- Starting JPEG Carving on '{disk_image_path}' ---")

    try:
        with open(disk_image_path, 'rb') as f:
            disk_data = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {disk_image_path}")
        return
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return

    print(f"Successfully read {len(disk_data) / (1024*1024):.2f} MB from the image.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")
    
    # NEW: --- Setup CSV Report ---
    report_path = os.path.join(output_dir, 'report.csv')
    csv_header = ['Filename', 'Start Offset', 'End Offset', 'Size (Bytes)', 'MD5 Hash']
    
    with open(report_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_header)

        # --- The Carving Loop ---
        found_files_count = 0
        current_search_offset = 0

        while True:
            header_offset = disk_data.find(JPEG_SOI, current_search_offset)

            if header_offset == -1:
                break
            
            print(f"\nFound a potential JPEG header at offset {header_offset}.")

            footer_offset = disk_data.find(JPEG_EOI, header_offset)

            if footer_offset == -1:
                print("  -> Found a header but no corresponding footer. Moving to next.")
                current_search_offset = header_offset + len(JPEG_SOI)
                continue
            
            footer_end_offset = footer_offset + len(JPEG_EOI)
            print(f"  -> Found a corresponding footer at offset {footer_offset}.")

            try:
                jpeg_data = disk_data[header_offset:footer_end_offset]
                
                # NEW: Calculate MD5 hash for integrity check
                md5_hash = hashlib.md5(jpeg_data).hexdigest()

                output_filename_leaf = f"recovered_{found_files_count}.jpg"
                output_filename_full = os.path.join(output_dir, output_filename_leaf)
                
                with open(output_filename_full, 'wb') as jpg_file:
                    jpg_file.write(jpeg_data)
                
                print(f"  -> SUCCESS: Carved {len(jpeg_data)} bytes and saved to '{output_filename_leaf}'")
                print(f"  -> MD5: {md5_hash}")

                # NEW: Write all our findings to the CSV report
                report_row = [
                    output_filename_leaf,
                    header_offset,
                    footer_end_offset,
                    len(jpeg_data),
                    md5_hash
                ]
                csv_writer.writerow(report_row)

                found_files_count += 1
                current_search_offset = footer_end_offset

            except Exception as e:
                print(f"  -> ERROR: Could not save file. {e}")
                current_search_offset = header_offset + len(JPEG_SOI)

    print(f"\n--- Carving Complete ---")
    print(f"Found and recovered a total of {found_files_count} JPEG file(s).")
    print(f"A detailed forensic report has been saved to '{report_path}'")


if __name__ == "__main__":
    IMAGE_FILE = "test_disk.dd"
    carve_files(IMAGE_FILE)