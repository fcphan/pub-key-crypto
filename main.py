import key_gen
import public_crypto
from sys import argv


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def main(argv):
    if len(argv) != 4:
        # Error message
        print(
            f'Error: Incorrect number of arguments. Supplied {len(argv)} arguments.')
        for a in argv:
            print(a)
        print('Please compile using the following:')
        print(color.BOLD +
              "python3 main.py <mode> <input> <output>" + color.END)
        print("\t<mode>: 'encrypt' or 'decrypt'")
        print("\t<input>: File to encrypt or decrypt")
        print("\t<output>: Output file to write results to.")
    else:
        # Grab mode and files supplied by user
        mode = argv[1]
        input_file = argv[2]
        output_file = argv[3]

        # Open input file and read in input
        try:
            f = open(input_file, mode='r')
            input_text = f.read()
            f.close()
        except:
            print(
                'Error: Could not find ' + color.GREEN + f'{input_file}' + color.END + ' or file has invalid characters used.')

        if mode == 'encrypt':
            print(f'Message: {input_text}')
            print('Generating public and private keys.')
            seed = input("Please enter a random seed: ")
            # Generate public and private keys - pubkey.txt and prikey.txt generated
            key_gen.key_gen(seed)

            # Retrieve public key information
            try:
                f = open('pubkey.txt', mode='r')
                public_key = f.readline()
                f.close()
            except:
                print('Error: Failed to find pubkey.txt')
            # Take key information and separate into p, g, and e2
            public_key = public_key.split()
            p = int(public_key[0])
            g = int(public_key[1])
            e2 = int(public_key[2])
            keys = {'p': p, 'g': g, 'e2': e2}

            res = input_text.split('\n')
            plaintext = res[0]
            # Encrypt
            ciphertext = public_crypto.encrypt(plaintext, keys)

            # Write encrypted text to file
            try:
                # Clear output file and write in new results
                f = open(output_file, mode='w').close()
                f = open(output_file, mode='a')
                print("\nGenerated ciphertext:")
                for c in ciphertext:
                    print(c)
                    f.write(f'{c[0]} {c[1]}\n')
                f.close()
            except:
                print(f'Error: Failed to find {output_file}.')
        elif mode == 'decrypt':
            # Retrieve private key information
            try:
                f = open('prikey.txt', mode='r')
                private_key = f.readline()
                f.close()
            except:
                print('Error: Failed to find prikey.txt')

            # Take key information and separate into p, g, and d
            private_key = private_key.split()
            p = int(private_key[0])
            g = int(private_key[1])
            d = int(private_key[2])
            keys = {'p': p, 'g': g, 'd': d}

            # Split string and store each item in list - will clean up in decrypt
            message = input_text.split()
            print('Ciphertext:')
            print(message)
            # Decrypt
            plain = public_crypto.decrypt(message, keys)

            # Write decrypted text to file
            try:
                # Clear output file and write in new results
                f = open(output_file, mode='w').close()
                f = open(output_file, mode='a')
                print("Decrypted ciphertext:")
                print(plain)
                f.write(plain)
                f.close()
            except:
                print(f'Error: Failed to find {output_file}.')


if __name__ == '__main__':
    main(argv)
