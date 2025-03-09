const TextAreaInput = ({ id, label, placeholder = '', value, rows = 20, onChange, error = false, errorMessage = '' }) => {
  return (
    <div>
      <label htmlFor={id} className="text-sm text-gray-200 block mb-2">
        {label}
      </label>
      <div className="relative">
        <textarea
          id={id}
          className={`w-full px-3 py-2 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200`}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          rows={rows}
          required
        />
      </div>

      {error && (
        <p className="text-sm text-red-500 mt-1">{errorMessage}</p>
      )}
    </div>
  );
};

export default TextAreaInput;
