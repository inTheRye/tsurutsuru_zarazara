# Tsurutsuru_zarazara backend

## Usage

```bash
$ cd tsurutsuru_zarazara
$ cd .deploy
$ ./local-up.sh
```

then access by curl

```bash
$ cd ../image_processing/dst
$ curl -X POST -F file=@01.png http://localhost:8080/data
"return json array data"
$ curl -X POST -F file=@01.png http://localhost:8080/wav
"return wave file"
```

## !!!! Caution !!!!

This docker container is not secure!
It is for prototype-use because it will expose the 8080 port for everyone!