import "./globals.css";

export const metadata = {
  title: "AI Code Tutor",
  description: "Next.js coding playground with JavaScript, Python and Java."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}