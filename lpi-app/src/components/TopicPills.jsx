import { useApp } from '../context/AppContext';
import { TOPICS } from '../utils/helpers';

export default function TopicPills() {
  const { state, save } = useApp();
  return (
    <div className="pills">
      <button className={!state.topicFilter ? 'active' : ''} onClick={() => save(s => ({ ...s, topicFilter: null, fcIdx: 0 }))}>All</button>
      {Object.entries(TOPICS).map(([num]) => (
        <button key={num} className={state.topicFilter === num ? 'active' : ''} onClick={() => save(s => ({ ...s, topicFilter: num, fcIdx: 0 }))}>T{num}</button>
      ))}
    </div>
  );
}
