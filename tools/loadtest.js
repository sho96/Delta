import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '20s',
  cloud: {
    // Project: Default project
    projectID: 3698370,
    // Test runs with the same name groups test runs together.
    name: 'Test (24/05/2024-00:28:22)'
  }
};

export default function() {
  http.get('https://quiz-eta-two.vercel.app/?noinit=true');
  sleep(1);
}