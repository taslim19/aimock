# UI Design Prompt for AI Mock Interview System

## Overall Design Requirements

Create a modern, professional, and user-friendly web interface for an AI-driven mock interview system with the following characteristics:

### Design Style
- **Modern and Clean**: Minimalist design with plenty of white space
- **Professional**: Suitable for job interview practice
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Color Scheme**: 
  - Primary: Blue (#3498db) for buttons and accents
  - Secondary: Gray (#95a5a6) for secondary actions
  - Success: Green (#27ae60) for positive actions
  - Background: Light gray (#f5f5f5) for page background
  - Cards: White (#ffffff) with subtle shadows
  - Text: Dark gray (#2c3e50) for headings, #333 for body text

### Typography
- Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Headings: Bold, larger sizes (h1: 3rem, h2: 2.5rem)
- Body: 1rem, line-height: 1.6
- Clear hierarchy with proper spacing

## Page Components

### 1. Navigation Bar
- **Style**: Dark background (#2c3e50), fixed at top
- **Content**: 
  - Left: Logo/Brand name "AI Mock Interview"
  - Right: Navigation links (Dashboard, Start Interview, Login/Register)
  - User name display when logged in
- **Behavior**: Hover effects on links, responsive menu for mobile

### 2. Homepage (Index)
- **Hero Section**:
  - Gradient background (purple/blue: #667eea to #764ba2)
  - Large heading: "AI-Driven Mock Interview System"
  - Subtitle explaining the purpose
  - Three feature cards in a grid:
    - Domain-Specific (with icon 🎯)
    - AI-Powered (with icon 🤖)
    - Detailed Feedback (with icon 📊)
  - Call-to-action buttons (Get Started, Login)
  
- **Info Section**:
  - "How It Works" heading
  - Four steps in a grid:
    - Step 1: Register & Login (numbered circle)
    - Step 2: Choose Domain
    - Step 3: Take Interview
    - Step 4: Get Feedback

### 3. Authentication Pages (Login/Register)
- **Layout**: Centered card on page
- **Card Style**: 
  - White background
  - Rounded corners (10px)
  - Box shadow for depth
  - Max width: 450px
  - Padding: 40px
- **Form Elements**:
  - Labels above inputs
  - Input fields: Full width, padding, border, rounded corners
  - Focus state: Blue border
  - Submit button: Full width, primary color
  - Link to alternate page (Login ↔ Register)
  - Error messages: Red background, visible below form

### 4. Dashboard
- **Header**: Welcome message with username
- **Statistics Grid**: Three stat cards showing:
  - Total Interviews (with icon 📊)
  - Completed Interviews (with icon ✅)
  - Average Score (with icon ⭐)
- **Action Button**: Large "Start New Interview" button
- **Recent Interviews Section**:
  - List of interview cards
  - Each card shows:
    - Domain name
    - Status badge (completed/in_progress)
    - Start date/time
    - Overall score (if completed)
    - Action button (View Results / Continue)

### 5. Domain Selection Page
- **Header**: "Select Interview Domain" with description
- **Domain Cards Grid**: 
  - Responsive grid (3-4 columns on desktop, 1 on mobile)
  - Each card:
    - Large icon (💻 for IT, 👥 for HR, 💰 for Finance, 📈 for Management)
    - Domain name
    - Description
    - "Start Interview" button
  - Hover effect: Slight lift with shadow
- **Loading Modal**: Shows spinner when generating questions

### 6. Interview Page
- **Header Section**:
  - Interview domain name
  - Progress bar (visual indicator)
  - Progress text ("Question X of Y")
  
- **Question Card**:
  - Question number and type badge
  - Question text (large, readable)
  - Answer textarea:
    - Large, multi-line
    - Placeholder text
    - Blue border on focus
  - Voice input controls:
    - "🎤 Start Recording" button
    - "⏹️ Stop Recording" button (hidden initially)
    - Recording status indicator (red dot when recording)
  - "Submit Answer" button

- **Evaluation Display** (shown after submission):
  - Scores grid showing:
    - Clarity score
    - Accuracy score
    - Communication score
    - Confidence score
    - Overall score (highlighted)
  - Feedback section with detailed text
  - Strengths box (green background)
  - Improvements box (yellow background)
  - "Next Question" button

### 7. Results Page
- **Header**: Interview results title with date/time
- **Overall Score Card**:
  - Large circular score display
  - Score value (large font, blue)
  - "Overall Score" label
  
- **Detailed Results**:
  - Each question in a card:
    - Question text
    - User's answer
    - Score breakdown (5 metrics)
    - Feedback text
    - Strengths list (green box)
    - Improvements list (yellow box)
  
- **Action Buttons**: 
  - "Start New Interview"
  - "Back to Dashboard"

## Interactive Elements

### Buttons
- **Primary**: Blue background, white text, rounded corners
- **Secondary**: Gray background
- **Success**: Green background
- **Hover**: Darker shade
- **Block**: Full width option
- **Large**: Bigger padding for important actions

### Cards
- White background
- Rounded corners (10px)
- Box shadow (subtle)
- Padding: 25-40px
- Hover effects where appropriate

### Forms
- Input fields: Clean borders, focus states
- Labels: Above inputs, clear typography
- Error states: Red borders, error messages
- Success states: Green indicators

### Status Indicators
- **Completed**: Green badge
- **In Progress**: Yellow badge
- **Recording**: Red dot with "Recording..." text
- **Stopped**: Green "Recording stopped" message

## Responsive Design

### Mobile (< 768px)
- Single column layouts
- Stacked navigation menu
- Full-width buttons
- Reduced font sizes
- Touch-friendly button sizes

### Tablet (768px - 1024px)
- 2-column grids where appropriate
- Adjusted spacing

### Desktop (> 1024px)
- Multi-column grids
- Optimal spacing
- Hover effects

## Animations & Transitions
- Smooth transitions on hover (0.3s)
- Progress bar animation
- Button state changes
- Modal fade in/out
- Loading spinner rotation

## Accessibility
- Semantic HTML
- Proper heading hierarchy
- Alt text for icons (where applicable)
- Keyboard navigation support
- Focus indicators
- Color contrast compliance

## Special Features

### Voice Input
- Microphone button with icon
- Visual recording indicator
- Real-time text display
- Status messages

### Progress Tracking
- Visual progress bar
- Percentage indicator
- Question counter

### Flash Messages
- Auto-dismiss after 5 seconds
- Color-coded (success/error)
- Non-intrusive placement

## Footer
- Simple, centered text
- Dark background matching navbar
- Copyright information

## Implementation Notes
- Use CSS Grid and Flexbox for layouts
- Modern CSS (no framework dependencies)
- Clean, maintainable code structure
- Consistent spacing system
- Reusable component styles

