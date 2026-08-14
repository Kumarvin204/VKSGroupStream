import '../styles/globals.css';
import Providers from '@/components/Providers';
import Navbar from '@/components/layout/Navbar';

export const metadata = {
  title: 'VKSGroupStream — YouTube Live Streaming Studio',
  description: 'Broadcast to YouTube Live with camera, screen share, and pre-recorded videos',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-surface-950 text-white min-h-screen antialiased selection:bg-brand-500/30">
        <Providers>
          <Navbar />
          <main className="pt-16 min-h-screen flex flex-col">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
