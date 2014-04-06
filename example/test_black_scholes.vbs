On Error Resume Next

Dim Pricer : Set Pricer = CreateObject("ppf.black_scholes")
Dim spot: spot = 42.
Dim strike: strike = 40.
Dim r: r = 0.1
Dim sig: sig = 0.2
Dim T: T= 0.5
Dim european_call: european_call = 1

Dim price : price = Pricer.OptionPrice(spot, strike, r, sig, T, european_call)

If Err.Number <> 0 Then
  WScript.Echo "Automation error : " & vbCr & Err.Number & _
               " (" & Hex(Err.Number) & ")" & vbCr & Err.Description
  Err.Clear
Else
  WScript.Echo price
End If

Set Pricer = Nothing
