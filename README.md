Reflection
1. Summary of the Project and the Problem It Solved
This project involved building a functional smart thermostat prototype using a Raspberry Pi. The goal was to demonstrate how embedded systems interact with sensors, user inputs, displays, and communication interfaces. The thermostat reads temperature data from an AHT20 sensor, updates a 16×2 LCD, controls LEDs to indicate heating and cooling behavior, and sends periodic status updates over UART. The project solved the challenge of coordinating multiple hardware components through a state machine architecture while maintaining reliable, real‑time behavior.

2. What I Did Particularly Well
I implemented a clean and maintainable state machine that controls the OFF, HEAT, and COOL modes. The LED fading logic, LCD update cycle, and UART communication were integrated smoothly. I also wrote readable, well‑structured code with clear separation of concerns, making the system easy to understand and extend.

3. Where I Could Improve
I could improve by optimizing the LCD refresh logic to reduce flicker and by exploring more advanced debouncing techniques for the physical buttons. Additionally, implementing asynchronous I/O or event‑driven patterns could make the system even more responsive and scalable.

4. Tools and Resources Added to My Support Network
Throughout this project, I strengthened my familiarity with:

Raspberry Pi GPIO and I²C interfaces

The Adafruit AHT20 sensor library

PWMLED control using gpiozero

UART communication and serial debugging tools

State machine design patterns for embedded systems

These tools will continue to support my work in future embedded and IoT projects.

5. Transferable Skills Gained
This project reinforced several transferable skills, including:

Designing modular, maintainable embedded software

Integrating hardware peripherals using I²C, GPIO, PWM, and UART

Applying state machine architectures to real‑time systems

Debugging hardware/software interactions

Documenting embedded systems for technical audiences

These skills apply directly to robotics, IoT development, real‑time systems, and future coursework.

6. How I Made the Project Maintainable, Readable, and Adaptable
I used clear function boundaries, descriptive naming conventions, and consistent formatting. The state machine encapsulates all mode‑transition logic, making the system easy to modify or extend. The LED, LCD, and UART behaviors are isolated into dedicated methods, improving readability and reducing coupling. This structure allows future developers—or my future self—to quickly understand and modify the system.# CS-350
