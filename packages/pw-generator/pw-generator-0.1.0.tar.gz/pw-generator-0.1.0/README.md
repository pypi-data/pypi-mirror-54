# pw-generator
Generate relatively secure passwords within python scripts.

The idea of the password generator, that produses relatively secure 
passwords, consisting from some english words and delimiters, and 
the wordlist itself were taken from passwdqc library.

## Code example

```
from pwgen import passphrase_gen, password_gen
from pwgen.exception import WeakPasswordException

password = passphrase_gen(5)
print(password)

password = password_gen(10)
print(password)

password = passphrase_gen(2)
""" Should get a WeakPasswordException """
```

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/pietro-a/pw-generator/blob/master/LICENSE)
file for details.

## Acknowledgments

Homepage of passwdqc library: http://openwall.com/passwdqc/
