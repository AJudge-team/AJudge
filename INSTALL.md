* osx에서 pyenv로 python 설치가 안되는 경우

```bash
CFLAGS="-I$(brew --prefix openssl)/include -I$(xcrun --show-sdk-path)/usr/include" \
LDFLAGS="-L$(brew --prefix openssl)/lib" \
pyenv install -v 3.5.0
```

* test 방법
```
python test.py
```