import os
import re
import argparse
import sys

def replace_twikoo_url(folder_path, dry_run=False):
    """
    替换文件夹中所有HTML文件中的Twikoo CDN链接
    
    Args:
        folder_path: 要处理的文件夹路径
        dry_run: 如果为True，只显示将要进行的更改而不实际修改文件
    """
    # 定义要查找和替换的字符串
    old_url = "//cdn.jsdelivr.net/npm/twikoo@1.6.39/dist/twikoo.all.min.js"
    new_url = "//registry.npmmirror.com/twikoo/1.6.44/files/dist/twikoo.min.js"
    
    # 统计信息
    total_files = 0
    modified_files = 0
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        return
    
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                total_files += 1
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否需要替换
                    if old_url in content:
                        # 进行替换
                        new_content = content.replace(old_url, new_url)
                        
                        if dry_run:
                            print(f"[预览] 将修改文件: {file_path}")
                            """
                            # 显示替换前后的对比
                            old_lines = [line for line in content.split('\n') if old_url in line]
                            new_lines = [line for line in new_content.split('\n') if new_url in line]
                            
                            if old_lines:
                                print("  替换前:")
                                for line in old_lines[:2]:  # 只显示前2行匹配的内容
                                    print(f"    {line.strip()}")
                            if new_lines:
                                print("  替换后:")
                                for line in new_lines[:2]:  # 只显示前2行匹配的内容
                                    print(f"    {line.strip()}")"""
                        else:
                            # 写入修改后的内容
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"[成功] 已修改文件: {file_path}")
                            modified_files += 1
                            
                except UnicodeDecodeError:
                    # 尝试其他编码
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                        
                        if old_url in content:
                            new_content = content.replace(old_url, new_url)
                            
                            if dry_run:
                                print(f"[预览] 将修改文件: {file_path}")
                            else:
                                with open(file_path, 'w', encoding='gbk') as f:
                                    f.write(new_content)
                                print(f"[成功] 已修改文件: {file_path}")
                                modified_files += 1
                                
                    except Exception as e:
                        print(f"[错误] 无法处理文件 {file_path}: {e}")
                        
                except Exception as e:
                    print(f"[错误] 处理文件 {file_path} 时出错: {e}")
    
    # 输出统计信息
    print("\n" + "="*50)
    print("替换完成!")
    print(f"扫描HTML文件总数: {total_files}")
    print(f"成功修改文件数: {modified_files}")
    
    if dry_run:
        print("注意: 这是预览模式，未实际修改任何文件")
        print("使用 --apply 参数来实际执行替换操作")

def main():
    parser = argparse.ArgumentParser(description='替换HTML文件中的Twikoo CDN链接')
    parser.add_argument('folder', help='要处理的文件夹路径')
    parser.add_argument('--apply', action='store_true', 
                       help='实际执行替换操作（默认是预览模式）')
    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，显示将要进行的更改但不实际修改文件')
    
    args = parser.parse_args()
    
    # 确定是否实际执行替换
    dry_run = not args.apply
    if args.dry_run:
        dry_run = True
    
    replace_twikoo_url(args.folder, dry_run)

if __name__ == "__main__":
    # 如果没有命令行参数，提示用户输入文件夹路径
    if len(sys.argv) == 1:
        folder_path = input("请输入要处理的文件夹路径: ")
        confirm = input("这是预览模式，只显示更改但不实际修改文件。继续吗? (y/n): ")
        if confirm.lower() in ['y', 'yes']:
            replace_twikoo_url(folder_path, dry_run=True)
            print("\n如果要实际执行替换，请使用: python script.py 文件夹路径 --apply")
        else:
            print("操作已取消")
    else:
        main()