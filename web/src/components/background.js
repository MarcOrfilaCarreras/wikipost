import React, { useEffect, useRef } from "react";

const Background = () => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        let width = window.innerWidth;
        let height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;

        const spacing = 20;
        let dots = [];

        const calculateDots = () => {
            dots = [];
            const columns = Math.ceil(width / spacing);
            const rows = Math.ceil(height / spacing);
            for (let row = 0; row < rows; row++) {
                for (let col = 0; col < columns; col++) {
                    const dotX = col * spacing + spacing / 2;
                    const dotY = row * spacing + spacing / 2;
                    dots.push({ x: dotX, y: dotY });
                }
            }
        };

        calculateDots();

        let mouseX = -1000, mouseY = -1000;

        const handleMouseMove = (event) => {
            mouseX = event.clientX;
            mouseY = event.clientY;
        };

        window.addEventListener("mousemove", handleMouseMove);

        const render = () => {
            ctx.clearRect(0, 0, width, height);

            dots.forEach(({ x, y }) => {
                const distance = Math.hypot(x - mouseX, y - mouseY);
                const intensity = Math.max(0, 1 - distance / 150);
                const opacity = 0.1 + intensity * 0.2;
                const scale = 1 + intensity * 0.5;
                const dotSize = 2 * scale;

                ctx.beginPath();
                ctx.arc(x, y, dotSize / 2, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255,255,255,${opacity})`;
                ctx.fill();
            });

            requestAnimationFrame(render);
        };

        render();

        const handleResize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
            calculateDots();
        };

        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    return <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" />;
};

export default Background;
