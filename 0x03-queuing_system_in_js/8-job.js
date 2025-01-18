export default function createPushNotificationsJobs(jobs, queue) {
    if (!Array.isArray(jobs)) {
      throw new Error('Jobs is not an array');
    }
  
    jobs.forEach((jobData, index) => {
      const job = queue.create('push_notification_code_3', jobData)
        .save((err) => {
          if (!err) {
            // Handle test mode explicitly
            if (queue.testMode.isActive) {
              job.id = index + 1; // Assign a mock ID
            }
            console.log(`Notification job created: ${job.id}`);
          } else {
            console.error(`Error creating job: ${err.message}`);
          }
        });
  
      // Add event listeners
      job.on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      });
  
      job.on('failed', (err) => {
        console.log(`Notification job ${job.id} failed: ${err}`);
      });
  
      job.on('progress', (progress) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
    });
  }
