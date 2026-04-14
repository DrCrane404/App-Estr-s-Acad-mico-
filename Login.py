import ttkbootstrap as tb

# Create a themed window
root = tb.Window(themename="superhero")
# Add buttons with different styles
btn1 = tb.Button(root, text="Success", bootstyle="success")
btn1.pack(pady=10)
btn2 = tb.Button(root, text="Info", bootstyle="info-outline")
btn2.pack(pady=10)
root.mainloop()

#Octavio