import { useState, useEffect } from 'react';

const SIZES = { sm: 32, md: 64, lg: 128 };
const MOODS = ['happy', 'celebrating', 'thinking', 'worried', 'studying', 'sleeping'];

export default function Mascot({ mood = 'happy', size = 'md', message }) {
  const [show, setShow] = useState(() => localStorage.getItem('lpi_mascot') !== 'off');
  const [msgVisible, setMsgVisible] = useState(!!message);

  useEffect(() => { if (message) { setMsgVisible(true); const t = setTimeout(() => setMsgVisible(false), 3000); return () => clearTimeout(t); } }, [message]);

  if (!show) return null;
  const px = SIZES[size] || SIZES.md;

  return (
    <div className="mascot-wrap" style={{ '--mascot-size': `${px}px` }}>
      <img
        src={`/mascot/mascot-${MOODS.includes(mood) ? mood : 'happy'}.png`}
        alt="Nix the penguin"
        className="mascot-img"
        width={px}
        height={px}
      />
      {message && msgVisible && (
        <div className="mascot-bubble">{message}</div>
      )}
    </div>
  );
}

export function useMascotVisible() {
  const [visible, setVisible] = useState(() => localStorage.getItem('lpi_mascot') !== 'off');
  const toggle = () => {
    const next = !visible;
    setVisible(next);
    localStorage.setItem('lpi_mascot', next ? 'on' : 'off');
  };
  return [visible, toggle];
}
