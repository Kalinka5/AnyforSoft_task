"""
Core commission calculation engine.
"""
from typing import List, Dict
from .data_loader import Partner

COMMISSION_RATE = 0.05

class CommissionCalculator:
    """
    Calculates commissions for all partners in an MLM network.
    """

    def __init__(self, partners: List[Partner], days_in_month: int):
        self._partners_map: Dict[int, Partner] = {p.id: p for p in partners}
        self._days_in_month = days_in_month
        self._adjacency_list = self._build_tree(partners)
        self._memo: Dict[int, float] = {}

    def _build_tree(self, partners: List[Partner]) -> Dict[int, List[int]]:
        """Builds an adjacency list for the partner hierarchy."""
        adj_list: Dict[int, List[int]] = {p.id: [] for p in partners}
        for p in partners:
            if p.parent_id is not None:
                adj_list[p.parent_id].append(p.id)
        return adj_list

    def _calculate_total_downline_revenue(self, partner_id: int) -> float:
        """
        Recursively calculates the total revenue from a partner and their downline
        using post-order traversal and memoization.
        """
        if partner_id in self._memo:
            return self._memo[partner_id]

        partner = self._partners_map[partner_id]
        
        # Start with the partner's own revenue
        total_revenue = partner.monthly_revenue

        # Add revenue from all children's downlines
        if partner_id in self._adjacency_list:
            for child_id in self._adjacency_list[partner_id]:
                total_revenue += self._calculate_total_downline_revenue(child_id)

        self._memo[partner_id] = total_revenue
        return total_revenue

    def calculate_commissions(self) -> Dict[int, float]:
        """
        Calculates the 5% commission for each partner based on the gross profit
        of all their descendants.
        """
        commissions: Dict[int, float] = {}
        
        # First, populate memoization table for all partners
        for partner_id in self._partners_map:
            if partner_id not in self._memo:
                self._calculate_total_downline_revenue(partner_id)

        # Then, calculate commissions
        for partner_id, partner in self._partners_map.items():
            
            # Commission is based on the revenue of descendants only.
            descendants_revenue = 0
            if partner_id in self._adjacency_list:
                for child_id in self._adjacency_list[partner_id]:
                    # The memoized value for a child includes the child's own revenue
                    # plus all of its own descendants.
                    descendants_revenue += self._memo.get(child_id, 0)
            
            print(f"descendants_revenue: {descendants_revenue} days: {self._days_in_month}")
            daily_gross_profit = descendants_revenue / self._days_in_month
            print(f"Partner {partner_id} has {daily_gross_profit} revenue")
            commissions[partner_id] = round(daily_gross_profit * COMMISSION_RATE, 2)
            print(f"Partner {partner_id} has {commissions[partner_id]} revenue")
            
        return commissions
