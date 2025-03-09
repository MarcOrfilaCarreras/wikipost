import React, { useState, useEffect, useRef } from 'react';
import TextInput from './text';

const CronJobGenerator = ({
  label = "CronJob Generator",
  onCronJobGenerated,
  defaultCronExpression = "* * * * *"
}) => {
  const [minute, setMinute] = useState('*');
  const [hour, setHour] = useState('*');
  const [dayOfMonth, setDayOfMonth] = useState('*');
  const [month, setMonth] = useState('*');
  const [dayOfWeek, setDayOfWeek] = useState('*');

  useEffect(() => {
    const parts = defaultCronExpression.split(' ');
    setMinute(parts[0] || '*');
    setHour(parts[1] || '*');
    setDayOfMonth(parts[2] || '*');
    setMonth(parts[3] || '*');
    setDayOfWeek(parts[4] || '*');
  }, [defaultCronExpression]);

  const cronExpression = `${minute} ${hour} ${dayOfMonth} ${month} ${dayOfWeek}`;

  const prevCronRef = useRef(cronExpression);

  useEffect(() => {
    if (cronExpression !== prevCronRef.current) {
      prevCronRef.current = cronExpression;
      if (onCronJobGenerated) {
        onCronJobGenerated(cronExpression);
      }
    }
  }, [cronExpression, onCronJobGenerated]);

  const handleInputChange = (setter) => (e) => {
    const value = e.target.value.trim();
    setter(value === '' ? '*' : value);
  };

  return (
    <div>
      <h1 className='text-sm text-gray-200 block mb-2'>{label}</h1>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6 mb-6">
        <TextInput
          id="minute"
          label="Minute"
          placeholder="*"
          value={minute}
          onChange={handleInputChange(setMinute)}
        />
        <TextInput
          id="hour"
          label="Hour"
          placeholder="*"
          value={hour}
          onChange={handleInputChange(setHour)}
        />
        <TextInput
          id="dayOfMonth"
          label="Day of Month"
          placeholder="*"
          value={dayOfMonth}
          onChange={handleInputChange(setDayOfMonth)}
        />
        <TextInput
          id="month"
          label="Month"
          placeholder="*"
          value={month}
          onChange={handleInputChange(setMonth)}
        />
        <TextInput
          id="dayOfWeek"
          label="Day of Week"
          placeholder="*"
          value={dayOfWeek}
          onChange={handleInputChange(setDayOfWeek)}
        />
      </div>

      <div className="bg-gray-700 px-3 py-2 rounded-lg">
        <code className="block text-lg font-mono text-gray-200">{cronExpression}</code>
      </div>
    </div>
  );
};

export default CronJobGenerator;
