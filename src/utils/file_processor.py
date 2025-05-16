import os

def process_file_or_folder(file_name):
    content_chunks = []

    if os.path.isfile(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                words = content.split()

                for i in range(0, len(words), 200):
                    chunk = ' '.join(words[i:i+200])
                    content_chunks.append({
                        "content": chunk,
                        "role": "user"
                    })
        except UnicodeDecodeError:
            print(f"Skipping file {file_name} due to encoding error.")
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")

    elif os.path.isdir(file_name):
        for root, dirs, files in os.walk(file_name):
            for file in files:
                if file.endswith(('.txt', '.png', '.jpeg', '.jpg')):
                    continue

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                        words = content.split()

                        for i in range(0, len(words), 200):
                            chunk = ' '.join(words[i:i+200])
                            content_chunks.append({
                                "content": chunk,
                                "role": "user"
                            })
                except UnicodeDecodeError:
                    print(f"Skipping file {file_path} due to encoding error.")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    else:
        print(f"{file_name} is neither a valid file nor a directory.")

    return content_chunks