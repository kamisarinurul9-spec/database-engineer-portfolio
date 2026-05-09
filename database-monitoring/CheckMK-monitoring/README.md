## run container checkmk-server
`docker compose up -d`
## Akses Dashboard
- http://10.204.20.137:8081/monitoring
<img width="1919" height="697" alt="Screenshot 2026-05-09 223531" src="https://github.com/user-attachments/assets/8fed3aa6-010d-4ecc-8949-d58d9de19459" /> <br />
username : `cmkadmin` <br />
password : `admin_password_anda` #sesuaikan password di docker compose <br />
## Tambahkan Host
Untuk memonitor server, kita perlu menginstal Checkmk Agent di target host tersebut.
- Unduh Agent: Di dashboard Checkmk, pergi ke Setup > Agents > Linux.
<img width="1570" height="942" alt="Screenshot 2026-05-09 224231" src="https://github.com/user-attachments/assets/4c5d4768-0aa9-4079-941f-a1b1f329a332" /> <br />

