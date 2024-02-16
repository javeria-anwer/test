using System;
using System.Collections.Generic;
using Product.Data.Model;

namespace Product.Data.Interface
{
    public interface IProducts
    {
        List<Products> GetAllProducts();
        Products GetProduct(int id);
    }
}
