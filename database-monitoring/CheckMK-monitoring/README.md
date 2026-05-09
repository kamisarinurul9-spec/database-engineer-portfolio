## run container checkmk-server
`docker compose up -d`
## Akses Dashboard
- http://10.204.20.137:8081/monitoring
<img width="1919" height="697" alt="Screenshot 2026-05-09 223531" src="https://github.com/user-attachments/assets/8fed3aa6-010d-4ecc-8949-d58d9de19459" /> <br />
username : `cmkadmin` <br />
password : `admin_password_anda` #sesuaikan password di docker compose <br />
## Tambahkan Host
Untuk memonitor server, kita perlu menginstal Checkmk Agent di target host tersebut.
- Di dashboard Checkmk, pergi ke Setup > Agents > Linux.
<img width="1570" height="942" alt="Screenshot 2026-05-09 224231" src="https://github.com/user-attachments/assets/4c5d4768-0aa9-4079-941f-a1b1f329a332" /> <br />
- Unduh agent dan Install di target
  http://10.204.20.137:8081/monitoring/check_mk/agents/check-mk-agent-2.2.0p47-1.noarch.rpm (misalnya OS target menggunakan CentOS, sesuaikan OS kita)
- Daftarkan Host
  Setup > Hosts > Add host <br />
<img width="1557" height="963" alt="Screenshot 2026-05-09 225353" src="https://github.com/user-attachments/assets/6af8760c-5ca9-49b0-b4d4-34f6d99b6235" /> <br />
- Masukkan Hostname dan IP Address.
- Save & go to service configuration.
- Checkmk akan melakukan service discovery secara otomatis.
- Accept all dan Activate Changes
- monitor > all hosts
<img width="1573" height="438" alt="Screenshot 2026-05-09 230745" src="https://github.com/user-attachments/assets/9a2c61d5-2a34-496d-8025-310e16ba7639" />  <br />

