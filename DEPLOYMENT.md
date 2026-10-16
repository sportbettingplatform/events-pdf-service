# Pokretanje i Jenkins

Projekat koristi Create React App (react-scripts 5.0.1), React 18 i TypeScript 4.9.

Lokalno: npm ci, zatim npm start (port 3000). npm run dev radi isto.
Jenkins: npm ci, zatim npm run build:prod. Izlaz je folder build.

Node 16.15+ je podržan; preporučena poslednja Node 16 verzija je 16.20.2.
package-lock.json treba komitovati zajedno sa package.json.

API podešavanja:
- REACT_APP_API_BASE_URL: osnovna adresa API servera, bez /api. Prazno znači isti domen.
- REACT_APP_PDF_LOCALE: jezik prevoda (cg).
- API_PROXY_TARGET: samo lokalni razvojni proxy za /api i /vc/api.

Za razvoj je pripremljen .env.development.local sa sportbook.topbetbo.com.
Taj fajl je ignorisan u Gitu. Na drugom računaru kopirati .env.example u .env.development.local.

Za produkciju u Jenkinsu podesiti REACT_APP_API_BASE_URL pre build-a (server mora dozvoljavati CORS),
ili ostaviti prazno i na hostingu proslediti /api i /vc/api na API server.
Razvojni proxy ne radi u produkciji. Za statički hosting objaviti sadržaj build foldera.

Provere: npm run typecheck, npm run lint, npm run build:prod.
