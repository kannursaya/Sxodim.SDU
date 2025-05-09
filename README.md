# Sxodim.SDU
HEAD

Event management system for SDU (Suleyman Demirel University) "WE HACK" Hackathon Project.

## Features

- User authentication (registration and login)
- Event management (create, view, and purchase tickets)
- Club management (create clubs and manage memberships)
- Ticket management (view and validate tickets)
- QR code generation for tickets

## Prerequisites

- Node.js (v14 or higher)
- MongoDB
- npm or yarn

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sxodim-sdu.git
cd sxodim-sdu
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory with the following variables:
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/sxodim-sdu
JWT_SECRET=your-super-secret-jwt-key
```

4. Start MongoDB server

5. Run the application:
```bash
# Development mode
npm run dev

# Production mode
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create new event
- `GET /api/events/:id` - Get event by ID
- `POST /api/events/:id/tickets` - Purchase event ticket

### Clubs
- `GET /api/clubs` - Get all clubs
- `POST /api/clubs` - Create new club
- `GET /api/clubs/:id` - Get club by ID
- `POST /api/clubs/:id/join` - Join a club

### Tickets
- `GET /api/tickets` - Get user's tickets
- `GET /api/tickets/:id` - Get specific ticket
- `POST /api/tickets/:id/validate` - Validate ticket

## License

MIT
=======
Sxodim.SDU is a web-based platform designed to enhance the student experience at SDU.The platform provides interactive features such as a game map, personalized social and academic tools, and real-time updates. It allows students to engage with campus activities, access various university resources, and track their academic progress.
>>>>>>> 723aeac5370cf83f75c4abbde5733946b61ef998
