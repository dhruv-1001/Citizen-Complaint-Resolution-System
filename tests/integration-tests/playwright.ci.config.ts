// The suite as the "Integration tests" workflow runs it on a GitHub runner
// (.github/workflows/integration-tests.yml): playwright.config.ts plus
//   - one retry, so a flaky test shows as `flaky` and does not fail a PR;
//     scripts/ci-compare.mjs counts flaky as a pass;
//   - traces, video and screenshots only for tests that fail, so the uploaded
//     report stays small enough to download;
//   - the GitHub reporter, which puts each failure on the PR's Files tab.
// The json reporter still writes report.json: ci-compare.mjs reads it.
import { defineConfig } from '@playwright/test';
import base from './playwright.config';

export default defineConfig({
  ...base,
  retries: 1,
  reporter: [
    ['list'],
    ['github'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'report.json' }],
  ],
  use: {
    ...base.use,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
  },
});
