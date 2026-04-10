import os
import re

replacements = {
    r'pi/sqrt\(8\)': 'pi/3',
    r'1\.1107\d*': '1.0472',
    'THE_AL_KASHI_ZETA_RESONANCE.md': 'THE_AL_KASHI_ZETA_RESONANCE.md',
    'Mathematical_Proof_Chapter_5_General_Resonance.md': 'Mathematical_Proof_Chapter_5_General_Resonance.md',
    'Al-Kashi Zeta Resonance': 'Al-Kashi Zeta Resonance',
    'Al-Kashi chord': 'Al-Kashi chord',
    'الكاشي': 'الكاشي',
}

def fortify_repository(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith(('.md', '.py', '.tex', '.html', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for pattern, replacement in replacements.items():
                        new_content = re.sub(pattern, replacement, new_content)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    repo_dir = r"c:\Users\allmy\Desktop\aaa\sn"
    fortify_repository(repo_dir)
