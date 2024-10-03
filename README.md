# Setup

Clone the repository
``` bash
git clone https://github.com/n3-v/mysocial
```

Deploy with Docker
``` bash
chmod +x ./build_docker.sh
```

``` bash
./build_docker.sh
```

# Solution

1. Sign up for an account
2. On your profile, upload a SVG XSS payload as your profile image, REF - https://infosecwriteups.com/stored-xss-using-svg-file-2e3608248fae
You can edit the example payload from "payload.svg". Before uploading, the webhook.site url should be replaced with your unique one (Generated here https://webhook.site)
3. Upon updating your PFP, the admin bot will visit your profile page and hopefully the XSS will be triggered with the cookie sent back to you
4. Check your webhook to see if you've received the cookie. If you used the payload in "payload.svg", you'll first have to base64 decode the cookie. Once received     we can replace it with ours.
5. Once admin, the flag will show in /profile/admin
