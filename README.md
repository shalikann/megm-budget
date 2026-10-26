# Stanford MEGM: Budget & Proposals

A password-protected site for tracking the MEGM annual budget, collecting event proposals, and recording purchases. It's a single `index.html` hosted on GitHub Pages, with data stored in a free Firebase Firestore database.

All proposals, purchases and budget figures are encrypted in the browser before they're saved. The database only ever holds scrambled data that can't be read without the club or finance password.

## One-time setup

### 1. Create the Firebase project

1. Go to https://console.firebase.google.com, click **Create a project**, and name it (for example `megm-budget`). Google Analytics isn't needed.
2. On the project overview page, click the **Web** icon (`</>`) to add a web app. Give it any nickname and skip Firebase Hosting.
3. Firebase shows a `firebaseConfig` block. Copy the `apiKey`, `authDomain`, `projectId` and `appId` values into `FIREBASE_CONFIG` near the top of the script in `index.html`.

The Firebase API key is meant to be public, so it's fine for it to be in a public repo. Access is controlled by the rules in step 2.

### 2. Set up the database

1. In the left menu, open **Build → Firestore Database** and click **Create database**. Choose a location near you and start in **production mode**.
2. Open the **Rules** tab, replace everything with the contents of `firestore.rules`, and click **Publish**.

### 3. Create the finance account

1. Open **Build → Authentication** and click **Get started**.
2. Under **Sign-in method**, enable **Email/Password**.
3. Under **Users**, click **Add user**:
   - Email: `megm-finance@megm-budget.app`
   - Password: the finance password (shared privately with the finance chairs and presidents)

The email doesn't need to be a real inbox, but it must match `FINANCE_EMAIL` in `index.html` and the email in `firestore.rules`. The password must be the finance password, because the site signs in with whatever is typed into the finance password box.

### 4. Publish on GitHub Pages

1. Create a new repository on GitHub (for example `megm-budget`) and upload `index.html`, `firestore.rules` and this README.
2. In the repo, open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select `main` and `/ (root)`, and save.
3. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`.
4. Back in Firebase, open **Authentication → Settings → Authorized domains** and add `<your-username>.github.io`.

### 5. Bring over your existing data

1. Open the site, sign in with the club password, then unlock **Finance & presidents**.
2. Go to **Budget allocations** and use **Restore from backup** with `megm-backup.json`.

Keep `megm-backup.json` out of the repo. It's encrypted, but there's no reason to publish it.

## Passwords

| Who | Password | Unlocks |
|---|---|---|
| All members | Club password (shared privately) | Budget overview and the proposal form |
| Finance chairs & presidents | Finance password (shared privately) | Proposals, purchases, budget allocations, CSV import |

The passwords are not stored in the code. The page holds encryption keys that can only be unlocked with them. To change a password, the encryption keys have to be regenerated, so ask whoever maintains the site (or Claude) to rebuild `index.html`. Download a backup first, since data encrypted with the old finance password won't open with the new one.

## Backups

Use **Budget allocations → Download backup** every so often. Firebase's free tier is reliable, but a backup protects against accidental deletes.
