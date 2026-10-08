"""Max-heap (priority queue) for appointments.

The appointment with the highest priority is always at the root.
Equal priorities are served in booking order (first come, first served),
using an arrival number as a tie-breaker.
"""

EMERGENCY = 3
URGENT = 2
NORMAL = 1
PRIORITY_NAMES = {EMERGENCY: "Emergency", URGENT: "Urgent", NORMAL: "Normal"}


class Appointment:
    def __init__(self, patient_id, doctor_id, priority, arrival):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.priority = priority
        self.arrival = arrival

    def __repr__(self):
        return (f"Appointment(patient={self.patient_id}, doctor={self.doctor_id}, "
                f"{PRIORITY_NAMES[self.priority]})")


class AppointmentHeap:
    def __init__(self):
        self._items = []      # heap stored in a list: children of i are 2i+1, 2i+2
        self._counter = 0     # arrival number given to each new appointment

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def _comes_before(self, a, b):
        """True if appointment a must be served before b."""
        if a.priority != b.priority:
            return a.priority > b.priority
        return a.arrival < b.arrival

    def add(self, patient_id, doctor_id, priority):
        """Insert at the end, then move up while it beats its parent. O(log n)."""
        self._counter += 1
        item = Appointment(patient_id, doctor_id, priority, self._counter)
        self._items.append(item)
        self._sift_up(len(self._items) - 1)
        return item

    def peek(self):
        """Look at the next appointment without removing it. O(1)."""
        return self._items[0] if self._items else None

    def serve(self):
        """Remove and return the highest-priority appointment. O(log n)."""
        if not self._items:
            return None
        top = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last   # move last item to the root ...
            self._sift_down(0)      # ... and push it down to its place
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._comes_before(self._items[i], self._items[parent]):
                self._items[i], self._items[parent] = self._items[parent], self._items[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._items)
        while True:
            best = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._comes_before(self._items[left], self._items[best]):
                best = left
            if right < n and self._comes_before(self._items[right], self._items[best]):
                best = right
            if best == i:
                break
            self._items[i], self._items[best] = self._items[best], self._items[i]
            i = best
