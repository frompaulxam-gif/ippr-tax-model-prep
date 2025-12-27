import wx
from tax_simulation import calculate_tax, DEFAULT_RULES

class TaxModelFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='IPPR Policy Sandbox', size=(500, 500))
        
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 1. SETUP INPUTS
        input_box = wx.StaticBox(self.panel, label="Policy Inputs")
        input_sizer = wx.StaticBoxSizer(input_box, wx.VERTICAL)
        
        input_sizer.Add(wx.StaticText(self.panel, label="Gross Income (£):"), 0, wx.ALIGN_LEFT)
        self.income_ctrl = wx.TextCtrl(self.panel, value="50000")
        input_sizer.Add(self.income_ctrl, 0, wx.EXPAND|wx.BOTTOM, 5)

        input_sizer.Add(wx.StaticText(self.panel, label="Adjust Basic Tax Rate (%):"), 0, wx.TOP, 10)
        self.rate_slider = wx.Slider(self.panel, value=20, minValue=0, maxValue=50, style=wx.SL_LABELS)
        self.rate_slider.Bind(wx.EVT_SLIDER, self.on_calculate)
        input_sizer.Add(self.rate_slider, 0, wx.EXPAND|wx.ALL, 5)

        self.main_sizer.Add(input_sizer, 0, wx.EXPAND|wx.ALL, 10)

        # 2. SETUP RESULTS
        result_box = wx.StaticBox(self.panel, label="Simulation Results")
        result_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        
        # Initial placeholder text
        self.result_label = wx.StaticText(self.panel, label="Status: Ready", style=wx.ALIGN_CENTER)
        
        font = self.result_label.GetFont()
        font.PointSize += 2
        font.MakeBold()
        self.result_label.SetFont(font)
        
        result_sizer.Add(self.result_label, 1, wx.EXPAND|wx.ALL, 20)
        self.main_sizer.Add(result_sizer, 1, wx.EXPAND|wx.ALL, 10)

        # 3. SETUP BUTTON
        calc_btn = wx.Button(self.panel, label="Run Simulation")
        calc_btn.Bind(wx.EVT_BUTTON, self.on_calculate)
        self.main_sizer.Add(calc_btn, 0, wx.ALIGN_CENTER|wx.BOTTOM, 20)
        
        self.panel.SetSizer(self.main_sizer)
        self.Show()

    def on_calculate(self, event):
        try:
            print("DEBUG: Calculation Started...") 
            
            income = float(self.income_ctrl.GetValue())
            custom_rate = self.rate_slider.GetValue() / 100.0
            
            rules = DEFAULT_RULES.copy()
            rules['basic_rate'] = custom_rate
            
            # UPDATED: We now unpack two values (Tax and NI)
            income_tax, ni_due = calculate_tax(income, rules)
            net_income = income - income_tax - ni_due
            
            # UPDATED: Display breakdown
            res_text = (
                f"Basic Rate Used: {int(custom_rate*100)}%\n\n"
                f"Income Tax: £{income_tax:,.2f}\n"
                f"National Insurance: £{ni_due:,.2f}\n"
                f"---------------------------\n"
                f"Net Income: £{net_income:,.2f}"
            )
            self.result_label.SetLabel(res_text)
            
            # Force Refresh
            self.result_label.Wrap(400)
            self.panel.Layout()
            
            print("DEBUG: Success!") 
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"DEBUG ERROR: {error_msg}")
            self.result_label.SetLabel(error_msg)
            self.panel.Layout()

if __name__ == '__main__':
    app = wx.App()
    frame = TaxModelFrame()
    app.MainLoop()