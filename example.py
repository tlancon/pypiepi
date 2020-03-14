import pypiepi as ppp

my_pie = 'data/cherry-pie.jpg'
manual_mask = ppp.segment_pie_manual(my_pie)
manual_mask = ppp.just_the_pie(manual_mask)
print(f"\nSimple pi calculation: {ppp.calculate_pi(manual_mask)}")
sim = ppp.SimulatePi(manual_mask, histories=31415, criterion=0.0000314, verbose=True)
print(f"\nRobust pi simulation:")
sim.run()
