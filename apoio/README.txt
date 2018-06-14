O script json2dot traduz um arquivo em formato json e imprime na tela
em formato dot correspondente.

$ ar2afd "(aa)*(b + aba)(aa)*" > afd.json
$ ./json2dot.sh afd.json > afd.dot
$ dot -Tpdf -o afd.pdf afd.dot

Se seu sistema não tiver o comando dot, instalar o graphviz.

$ sudo apt-get install graphviz

-----------------------------

O script afd2min.sh recebe um arquivo em formato json por parâmetro e imprime
na tela o automâto minimizado em formato dot.

$ ./min2afd other.json > other.dot
$ dot -Tpdf -o other.pdf other.dot
