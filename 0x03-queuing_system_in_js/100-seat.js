import express from 'express';
import kue from 'kue';
import { createClient } from 'redis';
import { promisify } from 'util';

// Create Redis Client
const client = createClient();
client.on('error', (err) => console.error('Redis Client Error:', err));

// Promisified Redis Methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Reservation State
let reservationEnabled = true;

// Redis Helper Functions
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
}

// Initialize Available Seats
(async () => {
  await reserveSeat(50); // Set initial seats to 50
})();

// Create Kue Queue
const queue = kue.createQueue();

// Express App
const app = express();
const PORT = 1245;

// Route: GET /available_seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route: GET /reserve_seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route: GET /process
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();

    if (currentSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      const newSeats = currentSeats - 1;
      await reserveSeat(newSeats);

      if (newSeats === 0) {
        reservationEnabled = false;
      }

      done();
    }
  });
});

// Start the Server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
