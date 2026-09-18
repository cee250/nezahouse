const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const booking = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const required = ['reference', 'checkin', 'checkout', 'roomName', 'fullName', 'email', 'phone'];
    const missing = required.filter((key) => !String(booking[key] || '').trim());

    if (missing.length) {
      return res.status(400).json({ error: `Missing required fields: ${missing.join(', ')}` });
    }

    const to = process.env.BOOKING_TO || process.env.GMAIL_USER;
    const user = process.env.GMAIL_USER;
    const appPassword = process.env.GMAIL_APP_PASSWORD;

    if (!to || !user || !appPassword) {
      console.error('Booking email variables are not configured.');
      return res.status(500).json({ error: 'Booking email is not configured on the server.' });
    }

    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: { user, pass: appPassword },
    });

    const subject = `New Grand Chalet Inn booking — ${booking.reference} — ${booking.roomName}`;
    const text = [
      'A new booking request was submitted on the Grand Chalet Inn website.',
      '',
      `Reference: ${booking.reference}`,
      `Room: ${booking.roomName}`,
      `Check-in: ${booking.checkin}`,
      `Check-out: ${booking.checkout}`,
      `Adults: ${booking.adults || '0'}`,
      `Children: ${booking.children || '0'}`,
      '',
      'Guest details',
      `Name: ${booking.fullName}`,
      `Email: ${booking.email}`,
      `Phone: ${booking.phone}`,
      `Country: ${booking.country || 'Not provided'}`,
      `Special requests: ${booking.requests || 'None'}`,
      '',
      `Submitted at: ${booking.createdAt || new Date().toISOString()}`,
    ].join('\n');

    await transporter.sendMail({
      from: `Grand Chalet Inn bookings <${user}>`,
      to,
      replyTo: booking.email,
      subject,
      text,
    });

    return res.status(200).json({ ok: true, reference: booking.reference });
  } catch (error) {
    console.error('Booking email failed:', error);
    return res.status(500).json({ error: 'The booking could not be emailed. Please try again.' });
  }
};
