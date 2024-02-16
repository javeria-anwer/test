using Product.Data.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Product.Data.Model;

namespace Product.Data.Repository
{
    public class ProductRepository : IProducts
    {
        List<Products> listProduct = new List<Products>
        {
            new Products{ProductId=1, Name="Product1", Description="Product 1"},
            new Products{ProductId=2, Name="Product2", Description="Product 2"},
            new Products{ProductId=3, Name="Product3", Description="Product 3"},
            new Products{ProductId=4, Name="Product4", Description="Product 4"},
            new Products{ProductId=5, Name="Product5", Description="Product 5"},
            new Products{ProductId=6, Name="Product6", Description="Product 6"},
            new Products{ProductId=7, Name="Product7", Description="Product 7"},
            new Products{ProductId=8, Name="Product8", Description="Product 8"},
            new Products{ProductId=9, Name="Product9", Description="Product 9"},
            new Products{ProductId=10, Name="Product10", Description="Product 10"},
        };
        public List<Products> GetAllProducts()
        {
            return listProduct;
        }

        public Products GetProduct(int id)
        {
            return listProduct.FirstOrDefault(x => x.ProductId == id) ?? new Products();
        }
    }
}
