# smart-kitchen-assistant

## Continuous Deployment with Expo EAS (Android Internal Testing)

This section outlines the steps to set up and use Expo Application Services (EAS) for continuous deployment to Android internal testing.

### Prerequisites

*   An Expo project set up in the `app/` directory.
*   Node.js and npm/yarn installed.
*   An Expo account.
*   A Google Play Console account.

### 1. Install EAS CLI

If you haven't already, install the EAS CLI globally:

```bash
npm install -g eas-cli
# or
yarn global add eas-cli
```

### 2. Log in to your Expo Account

Log in to your Expo account using the EAS CLI:

```bash
eas login
```
You will be prompted to enter your Expo account credentials.

### 3. Configure the Project for EAS Build

Navigate to your project's `app/` directory and configure it for EAS Build. If you don't have an `app.json` or `expo.json` file, EAS CLI can help generate it.

```bash
cd app
eas build:configure
```
Select "Android" when prompted. This command will create or update your `app.json`/`expo.json` with necessary build configurations and might also generate a default `eas.json` if one doesn't exist. We've already created a basic `eas.json` tailored for this project.

### 4. Understanding `eas.json`

The `eas.json` file defines different build and submit profiles. We've created one with the following relevant profiles:

*   **`build.preview`**: This profile is configured for internal distribution and builds an APK. This is typically used for internal testing.
*   **`build.production`**: This profile builds an Android App Bundle (AAB) suitable for production releases to the Google Play Store.
*   **`submit.production`**: This profile is used for submitting builds to app stores. It can be configured further to automate submissions.

Our `app/eas.json` looks like this:

```json
{
  "cli": {
    "version": ">= 5.9.3"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "android": {
        "buildType": "aab"
      }
    }
  },
  "submit": {
    "production": {}
  }
}
```

### 5. Start an Android Build for Internal Testing

To create a build for internal testing, use the `preview` profile:

```bash
cd app
eas build -p android --profile preview
```

This command will start the build process on EAS servers. You can monitor the build progress via the URL outputted in your terminal.

### 6. Submit to Google Play Internal Testing

Once the build is complete, EAS can help you submit it to the Google Play Store's internal testing track.

First, ensure you have set up your app on the Google Play Console and have API access configured for EAS Submit. This might involve creating a service account and providing EAS with a JSON key. Refer to the [EAS Submit documentation](https://docs.expo.dev/submit/android/) for detailed instructions on setting this up.

After configuring submission, you can submit a completed build using its ID or by specifying the `latest` build for the profile:

```bash
cd app
eas submit -p android --profile preview --latest
# or specify a build ID
# eas submit -p android --id <BUILD_ID>
```

Alternatively, if your `eas.json`'s `submit.production` (or a custom submit profile) is configured for internal testing, you can use that. For this example, we're using the build from the `preview` profile for submission.

### 7. Automating with CI/CD

For true continuous deployment, integrate these EAS commands into your CI/CD pipeline (e.g., GitHub Actions, GitLab CI). Your pipeline would typically:

1.  Checkout the code.
2.  Install dependencies.
3.  Run tests.
4.  Trigger an EAS build (`eas build -p android --profile preview --non-interactive`). The `--non-interactive` flag is crucial for CI environments.
5.  Once the build is successful, trigger an EAS submit (`eas submit -p android --profile preview --latest --non-interactive`).

You'll need to securely store your EAS token (and Google Service Account Key for submissions) as secrets in your CI/CD environment.

### Important Notes:

*   **`app.json`/`expo.json` Configuration**: Ensure your `app.json` or `expo.json` file in the `app/` directory has the correct `android.package` name (e.g., `com.yourcompany.yourapp`) and other necessary configurations before building.
*   **Credentials**: EAS Build will handle signing your Android app. You can let EAS generate new credentials or upload your own. For internal testing, EAS-generated credentials are often sufficient.
*   **Google Play Console Setup**: Your app must be set up in the Google Play Console, and the internal testing track must be configured before you can submit builds to it.