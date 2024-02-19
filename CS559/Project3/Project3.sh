chgrp treasure_group treasure.txt
chmod 660 treasure.txt

setfacl -m u:charlie:r-- treasure.txt
setfacl -m o::--- treasure.txt

getfacl treasure.txt
ls -l treasure.txt

getfacl treasure.txt
