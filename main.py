from the_super_tiny_compiler import compiler

def main():
    source_code = '(add 2 (subtract 4 2))'
    output = compiler(source_code)
    print(output)

if __name__ == '__main__':
    main()
