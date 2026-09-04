const nodemailer = require('nodemailer');

const json = (statusCode, body) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'Method not allowed' });
  }

  try {
    const booking = JSON.parse(event.body || '{}');
    const required = ['reference', 'checkin', 'checkout', 'roomName', 'fullName', 'email', 'phone'];
    const missing = required.filter((key) => !String(booking[key] || '').trim());
    if (missing.length) return json(400, { error: `Missing required fields: ${missing.join(', ')}` });

    const to = process.env.BOOKING_TO || process.env.GMAIL_USER;
    const user = process.env.GMAIL_USER;
    const appPassword = process.env.GMAIL_APP_PASSWORD;
    if (!to || !user || !appPassword) {
      console.error('Booking email variables are not configured.');
      return json(500, { error: 'Booking email is not configured on the server.' });
    }

    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: { user, pass: appPassword },
    });

    const subject = `New Neza House booking — ${booking.reference} — ${booking.roomName}`;
    const text = [
      'A new booking request was submitted on the Neza House website.',
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
      from: `Neza House bookings <${user}>`,
      to,
      replyTo: booking.email,
      subject,
      text,
    });

    return json(200, { ok: true, reference: booking.reference });
  } catch (error) {
    console.error('Booking email failed:', error);
    return json(500, { error: 'The booking could not be emailed. Please try again.' });
  }
};
