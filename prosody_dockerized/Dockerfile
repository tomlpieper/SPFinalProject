FROM prosody/prosody

# Create folders and the CA.key file
RUN cd /etc/prosody/certs && mkdir -p CA && cd CA && openssl genrsa -out CA.key -des -passout pass:password 2048 && openssl req -passin pass:password -x509 -sha256 -new -nodes -days 3650 -key CA.key -out CA.pem -subj "/C=DE/ST=LowerSaxony/L=Osnabrueck/O=DFKI/OU=SEE/CN=None" && mkdir localhost

# Copy the localhost.ext file
ADD ./localhost.ext /etc/prosody/certs/CA/localhost/
# Copy the prosody.cfg.lua file
ADD ./prosody.cfg.lua /etc/prosody/

# Create the localhost.key and localhost.csr files
RUN cd /etc/prosody/certs/CA/localhost && openssl genrsa -out localhost.key -des3 -passout pass:password 2048 && openssl req -passin pass:password -new -key localhost.key -out localhost.csr -subj "/C=DE/ST=LowerSaxony/L=Osnabrueck/O=DFKI/OU=SEE/CN=None" && openssl x509 -req -in localhost.csr -CA ../CA.pem -CAkey ../CA.key -CAcreateserial -days 3650 -sha256 -extfile localhost.ext -out localhost.crt -passin pass:password && openssl rsa -passin pass:password -in localhost.key -out localhost.decrypted.key && chmod -R 777 /etc/prosody

RUN prosodyctl register admin localhost adminpw
# RUN prosodyctl mod_pubsub create_node localhost NewNode "pubsub#access_model=open"
