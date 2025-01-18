import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    // Enter test mode
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    // Clear the queue and exit test mode
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 5678 to verify your account' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });

  it('should log the correct messages for job creation', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
    ];

    const logSpy = [];
    const consoleLog = console.log;
    console.log = (message) => logSpy.push(message); // Mock console.log

    createPushNotificationsJobs(jobs, queue);

    console.log = consoleLog; // Restore console.log

    expect(logSpy).to.include(`Notification job created: 1`);
  });
});
